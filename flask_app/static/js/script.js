function showForm() {
    document.getElementById('forSale').style.display = 'block';
}

function hideForm() {
    document.getElementById('forSale').style.display = 'none';
}

// function showFormEdit() {
//     document.getElementById('forSaleEdit').style.display = 'block';
// }

// function hideFormEdit() {
//     document.getElementById('forSaleEdit').style.display = 'none';
// }

// function showFormFromWatchlist() {
//     document.getElementById('forSaleFromWatchlist').style.display = 'block';
// }

// function hideFormFromWatchlist() {
//     document.getElementById('forSaleFromWatchlist').style.display = 'none';
// }

function floorCalc() {
    var x = document.getElementById("floorCalculator");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
