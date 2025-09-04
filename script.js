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

// function to add the outcome as information to each shot marker
function selectOutcome(outcome) {
    // selecting the last shot marker in the array 
    const lastShot = shots[shots.length - 1];
    // checking the array isn't empty
    if (lastShot) {
        // pushing the shot outcome to the array
        lastShot.push(outcome);
    }
}

// function to add the type of shot as information to each shot marker
function selectType(type) {
    // selecting the last shot marker in the array
    const lastShot = shots[shots.length - 1];
    // checking the array isn't empty
    if (lastShot) {
        // pushing the type of shot to the array
        lastShot.push(type);
    }
}

// function to add the position that took the shot as information to each shot marker
function selectPosition(position) {
    // selecting the last shot marker in the array
    const lastShot = shots[shots.length - 1];
    // checking the array isn't empty
    if (lastShot) {
        // pushing the position taking the shot to the array
        lastShot.push(position);
    }
    // now the popup can be hidden again
    document.getElementById('informationPopup').style.display = 'none';
}

// function to reset the pitch
function reset() {
    // redefining the shots array as an empty array
    shots = [];
    // find all shot markers
    const markers = document.querySelectorAll('.shot-marker');
    // remove each marker
    markers.forEach(marker => marker.remove());
}

// function to undo the last shot marker
function undo() {
    // ensuring the array isn't empty 
    if (shots.length > 0) {
        // remove the last shot marker from the array
        shots.pop();
    }
    // search for the pitch element in the HTML document
    const pitch = document.querySelector('.pitch');
    // search for the last shot marker within the pitch
    const lastShot = pitch.querySelector('.shot-marker:last-child');
    // check if the last shot marker exists
    if (lastShot) {
        // remove the marker visually
        lastShot.remove();
    }
}

// function to export all data as a csv file 
function exportShots() {
    // initialise csv content 
    let csvContent = 'x,y,timestamp,outcome,type,position\n';
    // loop through the store shot markers and their associated information
    shots.forEach(shot => {
        // access each item in the array
        const x = shot[0];
        const y = shot[1];
        const timestamp = shot[2];
        const outcome = shot[3];
        const type = shot[4];
        const position = shot[5];
        // add the data to the csv content
        csvContent += `${x},${y},${timestamp},${outcome},${type},${position}\n`;
    });
    // turn the csv file into a binary large object
    let blob = new Blob([csvContent], {type:'text/csv;charset=utf-8;' });
    // create an link element
    let link = document.createElement("a");
    // generate a url for the file
    let url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    // make the link invisible
    link.style.visibility = 'hidden';
    // add the link to ensure that it exists
    document.body.appendChild(link);
    // click the link to trigger to download
    link.click();
    // remove the link afterwards
    document.body.removeChild(link);
}




