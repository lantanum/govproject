// Открытие модального окна добавления ребёнка
document.getElementById("addChildBtn").addEventListener("click", function () {
    document.getElementById("addChildModal").style.display = "block";
});

// Закрытие модального окна добавления ребёнка
document.getElementById("closeModalBtn").addEventListener("click", function () {
    document.getElementById("addChildModal").style.display = "none";
});

// Открытие сканера QR-кодов
document.getElementById("scanQRCodeBtn").addEventListener("click", function () {
    document.getElementById("qrScannerModal").style.display = "block";

    const html5QrCode = new Html5Qrcode("reader");
    html5QrCode
        .start(
            { facingMode: "environment" },
            {
                fps: 10,
                qrbox: { width: 250, height: 250 },
            },
            (decodedText) => {
                // Отправляем данные на сервер для идентификации ребёнка
                fetch("/identify_child/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    body: new URLSearchParams({ qr_data: decodedText }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            document.getElementById(
                                "scanResult"
                            ).innerText = `Ребёнок: ${data.child_name}, Дата рождения: ${data.birth_date}`;
                        } else {
                            document.getElementById("scanResult").innerText = `Ошибка: ${data.error}`;
                        }
                    })
                    .catch((err) => console.error(err));
                html5QrCode.stop();
            },
            (errorMessage) => {
                console.error("QR Code scanning error: ", errorMessage);
            }
        )
        .catch((err) => {
            console.error("Unable to start QR Code scanner: ", err);
        });
});

// Закрытие модального окна сканера QR-кодов
document.getElementById("closeScannerBtn").addEventListener("click", function () {
    document.getElementById("qrScannerModal").style.display = "none";
    const html5QrCode = new Html5Qrcode("reader");
    html5QrCode.stop();
});
