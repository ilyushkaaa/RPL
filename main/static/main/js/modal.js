let selectedPlaceIds = new Set();
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM is ready.");

    const openModalLinks = document.querySelectorAll(".open-modal");
    const closeModalBtn = document.getElementById("close-modal");
    const modal = document.getElementById("modal");
    const modalContent = document.querySelector(".modal-content");
    const matchIdInput = document.getElementById('matchId');
    const buyButton = document.getElementById('buyButton');
    const cartCountElement = document.getElementById('cart-count');
    const deleteButtons = document.querySelectorAll(".buttonDelete");
    const confirmBuy = document.getElementById('confirmBuy');


// Обновите содержимое элемента <span> с использованием полученного значения


    $(".basket-container").on('click', function (e) {
        e.preventDefault();
        $('.basket-items').toggleClass('hidden')
    })


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

                                const rowCount = 5;
                                const placesPerRow = 10;

                                const placesMatrix = document.getElementById('placesMatrix');
                                let html = '';

                                for (let row = 1; row <= rowCount; row++) {
                                    html += `<div class="row">`;
                                    for (let place = 1; place <= placesPerRow; place++) {
                                        const curPlace = placesData.find(placeData => placeData.row === row && placeData.place === place);
                                        if (curPlace) {
                                            if (curPlace.is_not_available) {
                                                // Если is_not_available === true, делаем объект недоступным и меняем цвет
                                                html += `<button class="place unavailable" data-place-id="${curPlace.placeId}" disabled>${curPlace.place}</button>`;
                                            } else {
                                                // Иначе, объект доступен и имеет другой цвет
                                                html += `<button class="place" data-place-id="${curPlace.placeId}">${curPlace.place}</button>`;
                                            }
                                        } else {
                                            // Если объект не найден, отображаем "-"
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

    confirmBuy.addEventListener('click', function () {
        const csrfToken = getCSRFToken(); // Получаем CSRF-токен из cookie
        if (!csrfToken) {
            console.error('CSRF token not found.');
            return;
        }
        fetch(`/confirmBuy/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json",
            },
        })
            .then(response => {
                    if (response.ok) {
                        const basketItems = document.querySelectorAll('.basket-items li');
                        basketItems.forEach(item => {
                            item.remove();
                        });
                        let newNum = 0;

                        cartCountElement.textContent = newNum.toString()
                    } else {
                        console.error("Произошла ошибка при подтверждении покупки.");
                    }
                }
            )
            .catch(error => {
                console.error("Произошла ошибка при удалении билета: ", error);
            });
    })


    buyButton.addEventListener('click', () => {
        const csrfToken = getCSRFToken();
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
                const selectedPlaces = data.selectedPlaces;

                selectedPlaces.forEach(currentPlace => {
                    const listItem = `
        <li id = "${currentPlace.id}">
            ${currentPlace.teamHome} - ${currentPlace.teamGuest}<br>
            Сектор: ${currentPlace.sector}, Ряд: ${currentPlace.row}, Место: ${currentPlace.place}
            <button class="buttonDelete">Удалить</button>

        </li>
    `;

                    $('.basket-items ul').append(listItem);
                });


            })
            .catch(error => {
                console.error('Ошибка при отправке данных на сервер:', error);
            });
        modal.style.display = "none";
        let newNum = parseInt(cartCountElement.textContent) + selectedPlaceIds.size;

        cartCountElement.textContent = newNum.toString()


    });


    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            console.log("delete")
            const csrfToken = getCSRFToken(); // Получаем CSRF-токен из cookie
            if (!csrfToken) {
                console.error('CSRF token not found.');
                return;
            }

            const ticketId = this.getAttribute("data-id");

            // Отправить AJAX-POST-запрос на сервер для удаления билета
            fetch(`/delete_ticket/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ticketId: ticketId}),
            })
                .then(response => {
                    if (response.ok) {
                        const listItem = document.getElementById(ticketId);
                        if (listItem) {
                            listItem.remove();
                        }
                    } else {
                        console.error("Произошла ошибка при удалении билета.");
                    }
                })
                .catch(error => {
                    console.error("Произошла ошибка при удалении билета: ", error);
                });
            let newNum = parseInt(cartCountElement.textContent) - 1;

            cartCountElement.textContent = newNum.toString()
        });
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





