// ---------- Weekly grocery list ----------
// Replace the old openGroceryModal() and closeGroceryModal() at the bottom of dashboard.js with this block.
const GROCERY_KEY = 'fitforge_grocery_checked';
let groceryItems = [];

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const gKey = i => i.category + '|' + i.item;
function getChecked() { try { return new Set(JSON.parse(localStorage.getItem(GROCERY_KEY) || '[]')); } catch (e) { return new Set(); } }
function setChecked(set) { try { localStorage.setItem(GROCERY_KEY, JSON.stringify([...set])); } catch (e) {} }

async function openGroceryModal() {
  const modal = document.getElementById('groceryModal');
  const container = document.getElementById('groceryListContainer');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  container.innerHTML = '<p class="grocery-msg">Aggregating weekly ingredients...</p>';

  if (!container.dataset.bound) {           // bind once
    container.dataset.bound = '1';
    container.addEventListener('change', e => {
      if (!e.target.matches('input[type=checkbox]')) return;
      const set = getChecked();
      e.target.checked ? set.add(e.target.dataset.k) : set.delete(e.target.dataset.k);
      setChecked(set);
      e.target.closest('.grocery-item').classList.toggle('checked', e.target.checked);
      updateGroceryProgress();
    });
    modal.addEventListener('click', e => { if (e.target === modal) closeGroceryModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeGroceryModal(); });
  }

  try {
    const response = await fetch('/api/grocery-list');
    const data = await response.json();
    groceryItems = data.grocery_list || [];
    renderGrocery();
  } catch (error) {
    container.innerHTML = '<p class="grocery-msg">Error loading grocery list.</p>';
  }
}

function renderGrocery() {
  const container = document.getElementById('groceryListContainer');
  if (!groceryItems.length) {
    container.innerHTML = '<p class="grocery-msg">No meals generated yet. Create a meal plan first!</p>';
    updateGroceryProgress();
    return;
  }
  const done = getChecked(), groups = new Map();
  groceryItems.forEach(i => { if (!groups.has(i.category)) groups.set(i.category, []); groups.get(i.category).push(i); });

  let html = '';
  groups.forEach((items, cat) => {
    html += `<h3>${esc(cat)} <small>${items.length}</small></h3>`;
    items.forEach(i => {
      const on = done.has(gKey(i));
      html += `<label class="grocery-item ${on ? 'checked' : ''}">
        <input type="checkbox" data-k="${esc(gKey(i))}" ${on ? 'checked' : ''}>
        <span class="gi-box"></span><span class="gi-text">${esc(i.item)}</span></label>`;
    });
  });
  container.innerHTML = html;
  updateGroceryProgress();
}

function updateGroceryProgress() {
  const done = getChecked();
  const total = groceryItems.length, n = groceryItems.filter(i => done.has(gKey(i))).length;
  document.getElementById('groceryCount').textContent = `${n} / ${total} items`;
  document.getElementById('groceryBar').style.width = total ? (n / total * 100) + '%' : '0%';
}

function groceryText() {                     // only items you still need to buy
  const done = getChecked(), groups = new Map();
  groceryItems.forEach(i => { if (done.has(gKey(i))) return; if (!groups.has(i.category)) groups.set(i.category, []); groups.get(i.category).push(i.item); });
  if (!groups.size) return 'FitForge grocery list: everything is ticked off!';
  let t = 'FitForge weekly grocery list';
  groups.forEach((list, cat) => { t += `\n\n${cat}\n` + list.map(x => '- ' + x).join('\n'); });
  return t;
}

async function copyGroceryList(btn) {
  try { await navigator.clipboard.writeText(groceryText()); btn.textContent = 'Copied \u2713'; }
  catch (e) { btn.textContent = 'Copy failed'; }
  setTimeout(() => (btn.textContent = 'Copy list'), 1800);
}
function shareGroceryList() { window.open('https://wa.me/?text=' + encodeURIComponent(groceryText()), '_blank', 'noopener'); }
function clearGroceryChecks() { setChecked(new Set()); renderGrocery(); }

function closeGroceryModal() {
  document.getElementById('groceryModal').style.display = 'none';
  document.body.style.overflow = '';
}