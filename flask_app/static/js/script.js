function showForm() {
    document.getElementById('forSale').style.display = 'block';
}

function hideForm() {
    document.getElementById('forSale').style.display = 'none';
}

function floorCalc() {
    var x = document.getElementById("floorCalculator");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
