let selectedPlaceIds = new Set();
document.addEventListener("DOMContentLoaded", function () {
    const openModalLinks = document.querySelectorAll(".open-modal");
    const closeModalBtn = document.getElementById("close-modal");
    const modal = document.getElementById("modal");
    const modalContent = document.querySelector(".modal-content");
    const matchIdInput = document.getElementById('matchId');
    const buyButton = document.getElementById('buyButton');
    const cartCountElement = document.getElementById('cart-count');


    openModalLinks.forEach((openModalLink) => {
        openModalLink.addEventListener("click", function (event) {
            event.preventDefault();
            selectedPlaceIds = new Set();
            fetch('/check_authentication/')  // Это URL-маршрут для проверки авторизации
                .then(response => response.json())
                .then(data => {
                    if (data.authenticated) {
                        modalContent.querySelector("p").textContent = "Сектор " + openModalLink.getAttribute("data-text");
                        const matchId = matchIdInput.getAttribute('data-match-id');
                        const sectorNum = openModalLink.getAttribute("data-text");
                        modal.style.display = "block";
                        fetch(`/get_places/?sector_num=${sectorNum}&match_id=${matchId}`)
                            .then(response => response.json())
                            .then(data => {
                                const placesData = data.places;

                                const rowCount = 5; // Например, 2 ряда
                                const placesPerRow = 10; // Например, 3 места в каждом ряду

                                const placesMatrix = document.getElementById('placesMatrix');
                                let html = '';

                                for (let row = 1; row <= rowCount; row++) {
                                    html += `<div class="row">`;
                                    for (let place = 1; place <= placesPerRow; place++) {
                                        const curPlace = placesData.find(placeData => placeData.row === row && placeData.place === place);
                                        if (curPlace) {

                                            html += `<div class="place" data-place-id="${curPlace.placeId}">${curPlace.place}</div>`;
                                        } else {
                                            html += `<div class="place">-</div>`;
                                        }
                                    }
                                    html += `</div>`;
                                }

                                placesMatrix.innerHTML = html;


                                const placeElements = document.querySelectorAll('.place');

                                placeElements.forEach(placeElement => {
                                    placeElement.addEventListener('click', () => {
                                        const placeId = placeElement.getAttribute('data-place-id');
                                        console.log(placeId)

                                        if (placeElement.classList.contains('selected-place')) {
                                            placeElement.classList.remove('selected-place');
                                            placeElement.classList.add('default-place');
                                        } else {

                                            placeElement.classList.remove('default-place');
                                            placeElement.classList.add('selected-place');
                                        }

                                        handlePlaceClick(placeId, selectedPlaceIds);
                                    });
                                });
                            });
                    } else {
                        // Если пользователь не авторизован, выводим сообщение
                        alert('Для покупки билетов необходимо авторизоваться.');
                    }
                });

        });
    });

    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("mousedown", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    function getCSRFToken() {
        const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
        if (csrfToken) {
            return csrfToken.split('=')[1];
        }
        return null;
    }


    buyButton.addEventListener('click', () => {
        const csrfToken = getCSRFToken(); // Получаем CSRF-токен из cookie
        if (!csrfToken) {
            console.error('CSRF token not found.');
            return;
        }

        console.log("ededededededede")
        fetch('/process_selected_places/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Добавляем CSRF-токен в заголовки запроса
            },
            body: JSON.stringify({placeIds: Array.from(selectedPlaceIds)}), // Преобразуем Set в массив
        })
            .then(response => response.json())
            .then(data => {
                // Обработка ответа от сервера
            })
            .catch(error => {
                console.error('Ошибка при отправке данных на сервер:', error);
            });
        modal.style.display = "none";
        let newNum = parseInt(cartCountElement.textContent) + selectedPlaceIds.size;

        cartCountElement.textContent = newNum.toString()

    });
});

const modalScrollableContent = document.querySelector('.modal-scrollable-content');
const modal = document.getElementById('modal');
modal.style.marginTop = `-${modalScrollableContent.clientHeight / 2}px`;


// Обработчик клика на месте
function handlePlaceClick(placeId) {
    if (selectedPlaceIds.has(placeId)) {
        // Если место уже было выбрано, удаляем его из набора
        selectedPlaceIds.delete(placeId);
    } else {
        // Если место еще не было выбрано, добавляем его в набор
        selectedPlaceIds.add(placeId);
    }

    console.log("Выбранные места:", Array.from(selectedPlaceIds));
}





