(function(){
  const table = document.getElementById('leaderboard');
  const searchBox = document.getElementById('searchBox');
  if(!table) return;
  const ths = table.querySelectorAll('th');
  let sortState = { key: 'rank', dir: 'asc' };

  function getCellValue(tr, key){
    const td = tr.querySelector('td[data-key="'+key+'"]');
    if(!td) return '';
    const v = td.getAttribute('data-value');
    if(v === '') return '';
    return v;
  }

  function compareRows(a, b, key, type){
    const va = getCellValue(a, key);
    const vb = getCellValue(b, key);
    if(type === 'number'){
      const na = parseFloat(va);
      const nb = parseFloat(vb);
      if(isNaN(na) && isNaN(nb)) return 0;
      if(isNaN(na)) return 1;
      if(isNaN(nb)) return -1;
      return na - nb;
    } else {
      return String(va).localeCompare(String(vb));
    }
  }

  function sortBy(key, type){
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    if(sortState.key === key){
      sortState.dir = sortState.dir === 'asc' ? 'desc' : 'asc';
    } else {
      sortState.key = key;
      sortState.dir = 'asc';
    }
    rows.sort(function(a,b){
      const cmp = compareRows(a,b,key,type);
      return sortState.dir === 'asc' ? cmp : -cmp;
    });
    rows.forEach(r => tbody.appendChild(r));
    ths.forEach(th => {
      if(th.getAttribute('data-key') === key){
        th.textContent = th.textContent.replace(/\s*[▴▾]$/, '') + (sortState.dir === 'asc' ? ' ▴' : ' ▾');
      } else {
        th.textContent = th.textContent.replace(/\s*[▴▾]$/, '') + ' ▾';
      }
    });
  }

  ths.forEach(th => {
    const key = th.getAttribute('data-key');
    const type = th.getAttribute('data-type') || 'string';
    th.addEventListener('click', ()=> sortBy(key, type));
  });

  // initial sort
  sortBy('rank','number');

  // search/filter functionality
  function filterRows(query){
    const q = (query || '').trim().toLowerCase();
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.forEach(r => {
      const username = (r.querySelector('td[data-key="username"]').textContent || '').toLowerCase();
      const full = (r.querySelector('td[data-key="full_name"]').textContent || '').toLowerCase();
      if(q === '' || username.includes(q) || full.includes(q)){
        r.style.display = '';
      } else {
        r.style.display = 'none';
      }
    });
  }

  if(searchBox){
    searchBox.addEventListener('input', function(e){
      filterRows(e.target.value);
    });
  }
})();
