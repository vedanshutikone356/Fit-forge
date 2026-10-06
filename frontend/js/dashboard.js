// FitForge Dashboard Interactive Logic

document.addEventListener("DOMContentLoaded", async () => {
  // Retrieve saved user ID or default to 1
  let userId = localStorage.getItem("fitforge_user_id");
  if (!userId) {
    userId = 1; // Fallback demo user
  }

  await loadUserProfile(userId);
  await loadWorkoutPlan(userId);
  await loadNutritionPlan(userId);
  await loadProgressChart(userId);
  await loadProductivityGoals(userId);

  // Setup Activity Logging Form Handler
  document.getElementById("quickLogForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const steps = parseInt(document.getElementById("logSteps").value) || null;
    const sleep = parseFloat(document.getElementById("logSleep").value) || null;
    const water = parseFloat(document.getElementById("logWater").value) || null;
    const stress = parseInt(document.getElementById("logStress").value) || null;

    try {
      const response = await fetch("/api/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(userId),
          steps: steps,
          sleep_hours: sleep,
          water_liters: water,
          stress_level: stress
        })
      });
      const data = await response.json();
      if (data.status === "success") {
        alert("Daily activity logged successfully!");
        await loadProgressChart(userId);
      }
    } catch (err) {
      console.error("Error logging activity:", err);
    }
  });

  // Setup Add Productivity Goal Handler
  document.getElementById("addGoalBtn").addEventListener("click", async () => {
    const titleInput = document.getElementById("newGoalTitle");
    const title = titleInput.value.trim();
    if (!title) return;

    try {
      const response = await fetch("/api/goals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: parseInt(userId), title: title })
      });
      if (response.ok) {
        titleInput.value = "";
        await loadProductivityGoals(userId);
      }
    } catch (err) {
      console.error("Error adding goal:", err);
    }
  });
});

// Fetch & Render User Profile Metrics
async function loadUserProfile(userId) {
  try {
    const res = await fetch(`/api/user/${userId}`);
    if (!res.ok) return;
    const user = await res.json();
    const m = user.metrics;

    document.getElementById("userGreeting").innerText = `Good Day, ${user.name}! 🚀`;
    document.getElementById("userGoalSub").innerText = `Goal: ${user.fitness_goal} | BMI: ${m.bmi} (${m.bmi_category})`;
    
    document.getElementById("calVal").innerText = `${m.target_calories} kcal`;
    document.getElementById("calSub").innerText = `BMR: ${m.bmr} | TDEE: ${m.tdee} kcal`;

    document.getElementById("protVal").innerText = `${m.target_protein} g`;
    document.getElementById("macroSub").innerText = `Carbs: ${m.target_carbs}g | Fat: ${m.target_fat}g`;

    document.getElementById("stepVal").innerText = `${user.avg_steps}`;
    document.getElementById("stepSub").innerText = `Target: ${m.target_steps} steps`;

    document.getElementById("waterVal").innerText = `${m.target_water} L`;

    // Render Stress Tips
    const tipsContainer = document.getElementById("stressTipsList");
    tipsContainer.innerHTML = "";
    if (m.stress_tips && m.stress_tips.length > 0) {
      m.stress_tips.forEach(tip => {
        const li = document.createElement("li");
        li.innerText = `💡 ${tip}`;
        tipsContainer.appendChild(li);
      });
    }
  } catch (err) {
    console.error("Failed to load user profile:", err);
  }
}

// Fetch & Render Workout Schedule
async function loadWorkoutPlan(userId) {
  try {
    const res = await fetch(`/api/workout/${userId}`);
    if (!res.ok) return;
    const plan = await res.json();

    document.getElementById("workoutSplitName").innerText = plan.split_name;
    const container = document.getElementById("workoutExerciseList");
    container.innerHTML = "";

    for (const [day, dayData] of Object.entries(plan.schedule)) {
      const dayBox = document.createElement("div");
      dayBox.className = "exercise-item";
      
      let exercisesHtml = dayData.exercises.map(ex => 
        `<div class="exercise-details">• ${ex.name} — ${ex.sets} sets x ${ex.reps} (${ex.target})</div>`
      ).join("");

      dayBox.innerHTML = `
        <div class="exercise-header">
          <span>${day}</span>
          <span style="color: var(--accent-green); font-size: 0.85rem;">${dayData.focus}</span>
        </div>
        ${exercisesHtml}
      `;
      container.appendChild(dayBox);
    }
  } catch (err) {
    console.error("Failed to load workout plan:", err);
  }
}

// Fetch & Render Pandas Nutrition Plan
async function loadNutritionPlan(userId) {
  try {
    const res = await fetch(`/api/nutrition/${userId}`);
    if (!res.ok) return;
    const nut = await res.json();

    document.getElementById("dietPrefTag").innerText = nut.diet_preference;
    const container = document.getElementById("nutritionMealList");
    container.innerHTML = "";

    for (const [mealName, info] of Object.entries(nut.meals)) {
      const mealBox = document.createElement("div");
      mealBox.className = "meal-item";
      mealBox.innerHTML = `
        <div class="exercise-header">
          <span>${mealName.toUpperCase()}</span>
          <span style="color: var(--accent-cyan); font-size: 0.85rem;">${info.calories} kcal</span>
        </div>
        <div class="exercise-details" style="font-weight: 600; color: #f3f4f6;">${info.item}</div>
        <div class="exercise-details">Protein: ${info.protein_g}g | Carbs: ${info.carbs_g}g | Fat: ${info.fat_g}g</div>
      `;
      container.appendChild(mealBox);
    }
  } catch (err) {
    console.error("Failed to load nutrition plan:", err);
  }
}

// Fetch & Render Matplotlib Chart
async function loadProgressChart(userId) {
  try {
    const res = await fetch(`/api/progress/${userId}`);
    if (!res.ok) return;
    const data = await res.json();

    const chartContainer = document.getElementById("chartContainer");
    if (data.chart_base64) {
      chartContainer.innerHTML = `<img src="${data.chart_base64}" alt="Weekly Progress Chart">`;
    }
  } catch (err) {
    console.error("Failed to load chart:", err);
  }
}

// Fetch & Render Productivity Checklist
async function loadProductivityGoals(userId) {
  try {
    const res = await fetch(`/api/goals/${userId}`);
    if (!res.ok) return;
    const data = await res.json();

    const container = document.getElementById("productivityList");
    container.innerHTML = "";

    if (data.goals.length === 0) {
      container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem;">No goals added for today yet.</p>`;
      return;
    }

    data.goals.forEach(goal => {
      const item = document.createElement("div");
      item.className = "goal-item";
      item.style.display = "flex";
      item.style.justifySpaceBetween = "space-between";
      item.style.alignItems = "center";

      const isChecked = goal.completed ? "checked" : "";
      const textStyle = goal.completed ? "line-through; color: var(--text-muted)" : "";

      item.innerHTML = `
        <span style="text-decoration: ${textStyle}">${goal.title}</span>
        <input type="checkbox" ${isChecked} onchange="toggleGoal(${goal.id}, this.checked)">
      `;
      container.appendChild(item);
    });
  } catch (err) {
    console.error("Failed to load goals:", err);
  }
}

// Global Toggle Goal Completion
async function toggleGoal(goalId, completed) {
  try {
    await fetch(`/api/goals/${goalId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: completed ? 1 : 0 })
    });
  } catch (err) {
    console.error("Failed to toggle goal:", err);
  }
}
async function openGroceryModal() {
  document.getElementById('groceryModal').style.display = 'block';
  const container = document.getElementById('groceryListContainer');
  container.innerHTML = '<p>Aggregating weekly ingredients...</p>';

  try {
    const response = await fetch('/api/grocery-list');
    const data = await response.json();

    if (data.grocery_list && data.grocery_list.length > 0) {
      let html = '';
      let currentCategory = '';

      data.grocery_list.forEach(item => {
        if (item.category !== currentCategory) {
          currentCategory = item.category;
          html += `<h3>${currentCategory}</h3>`;
        }
        html += `
          <label class="grocery-item">
            <input type="checkbox" onchange="this.parentElement.classList.toggle('checked')">
            <span>${item.item}</span>
          </label><br>
        `;
      });
      container.innerHTML = html;
    } else {
      container.innerHTML = '<p>No meals generated yet. Create a meal plan first!</p>';
    }
  } catch (error) {
    container.innerHTML = '<p>Error loading grocery list.</p>';
  }
}

function closeGroceryModal() {
  document.getElementById('groceryModal').style.display = 'none';
}