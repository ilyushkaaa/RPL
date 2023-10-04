document.addEventListener("DOMContentLoaded", function () {
    const openModalLinks = document.querySelectorAll(".open-modal");
    const closeModalBtn = document.getElementById("close-modal");
    const modal = document.getElementById("modal");
    const modalContent = document.querySelector(".modal-content");
    const matchIdInput = document.getElementById('matchId');
    openModalLinks.forEach((openModalLink) => {
        openModalLink.addEventListener("click", function (event) {
            event.preventDefault();
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
                                html += `<div class="place" data-place-id="${curPlace.place}">${curPlace.place}</div>`;
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

                            if (placeElement.classList.contains('selected-place')) {
                                placeElement.classList.remove('selected-place');
                                placeElement.classList.add('default-place');
                            } else {
                                placeElement.classList.remove('default-place');
                                placeElement.classList.add('selected-place');
                            }

                            handlePlaceClick(placeId);
                        });
                    });
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
});

const modalScrollableContent = document.querySelector('.modal-scrollable-content');
const modal = document.getElementById('modal');
modal.style.marginTop = `-${modalScrollableContent.clientHeight / 2}px`;

function handlePlaceClick(placeId) {
    // Ваш код для обработки клика на месте
    // Например, вы можете выполнить какие-либо действия при клике на месте
    console.log(`Выбрано место с идентификатором: ${placeId}`);
}
