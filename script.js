let shots = []; // global array to store all the recorded shot coordinates


// function to get called on the mouse event of clicking
function recordShot(event) {
    // normalising the x coordinate of the event
    const x = (event.offsetX / event.target.offsetWidth) * 68;
    // flipping and scaling y 
    const y_flipped = 105 - (event.offsetY / event.target.offsetHeight) * 105;
    // capture the current timestamp
    const timestamp = new Date().toISOString();
    // saving the coordinates and timestamp to the shots array 
    shots.push([x, y_flipped, timestamp])
    // creating a visual marker on the football pitch
    let marker = document.createElement('div')
    // adding a class name for styling in order to ensure that shot markers appear on the pitch
    marker.className = 'shot-marker'
    // positioning the marker horizontally 
    marker.style.left = (x / 68 * 100) + '%';
    // positioning the marker vertically 
    const y_original_percentage = (event.offsetY / event.target.offsetHeight) * 100;
    marker.style.top = y_original_percentage + '%';
    // add a marker to the element
    event.target.appendChild(marker);

    const informationPopup = document.getElementById('informationPopup');
    informationPopup.style.display = 'block';
}




