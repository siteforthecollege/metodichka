'use strict';
document.querySelectorAll('[data-visit-counter]').forEach(image => {
  const showUnavailable = () => {
    const message = document.createElement('span');
    message.textContent = 'Счётчик временно недоступен';
    image.replaceWith(message);
  };
  image.addEventListener('error', showUnavailable, {once: true});
  if (image.complete && image.naturalWidth === 0) showUnavailable();
});
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => {
  const details = [...document.querySelectorAll('details')];
  const states = details.map(item => item.open);
  details.forEach(item => { item.open = true; });
  const restore = () => details.forEach((item, index) => { item.open = states[index]; });
  window.addEventListener('afterprint', restore, {once: true});
  window.print();
}));
const feedback = document.getElementById('feedback');
if (feedback) feedback.addEventListener('submit', event => {
  event.preventDefault();
  if (!feedback.reportValidity()) return;
  const data = new FormData(feedback);
  const message = String(data.get('message') || '').trim();
  if (message.length < 10) {
    document.getElementById('feedback-status').textContent = 'Опишите вопрос подробнее: не менее 10 символов.';
    return;
  }
  const params = new URLSearchParams({title: String(data.get('topic')), body: 'Материал: '+(String(data.get('material')||'').trim()||'Общий вопрос')+'\n\n'+message});
  const url = 'https://github.com/'+feedback.dataset.repository+'/issues/new?'+params.toString();
  const status = document.getElementById('feedback-status');
  status.replaceChildren();
  const a = document.createElement('a');
  a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
  a.textContent = 'Открыть подготовленное обращение на GitHub';
  status.append(a);
  window.open(url, '_blank', 'noopener,noreferrer');
});
