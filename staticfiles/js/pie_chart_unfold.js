document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("userChart").getContext("2d");

    // Fetch data from the global JavaScript variable set in the template
    const userData = JSON.parse(document.getElementById("userData").textContent);

    const userChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Superusers", "Clients", "Staff"],
            datasets: [
                {
                    label: "User Distribution",
                    data: [userData.total_superusers, userData.total_clients, userData.total_staff],
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                    hoverOffset: 4,
                },
            ],
        },
    });
});
