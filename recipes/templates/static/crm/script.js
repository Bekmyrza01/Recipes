
const objects = document.querySelectorAll('.object');

// Добавить обработчик события "click" к каждому объекту
objects.forEach(function(object) {
  object.addEventListener('click', function() {
    // Получить ID объекта из атрибута "data-object-id"
    const objectId = object.dataset.objectId;