// "option" for "select" fields in Prediction-Form
const occupationOptions = ["Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse", "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager"];
const genderOptions = ["Male", "Female"];
const bmiOptions = ["Normal", "Underweight", "Overweight", "Obese"];

// Disorder Description
const disorderInfo = {
    "-": {
        description: "Please fill out the form and click 'Predict' to see the result.",
    },
    "no disorder": {
        description: "No disorder detected. You have a healthy sleep pattern.",
        backgroundColor: "green"
    },
    "sleep apnea": {
        description: "Sleep Apnea is a serious sleep disorder where your breathing repeatedly stops and starts during sleep.",
        causes: [
            "Obesity",
            "Nasal obstruction",
            "Family history of sleep apnea"
        ],
        treatment: [
            "CPAP (Continuous Positive Airway Pressure) therapy",
            "Weight loss",
            "Surgery (in extreme cases)"
        ],
        backgroundColor: "red"
    },
    "insomnia": {
        description: "Insomnia is the inability to fall or stay asleep. It's a common sleep disorder.",
        causes: [
            "Stress or anxiety",
            "Poor sleep environment",
            "Chronic pain"
        ],
        treatment: [
            "Cognitive Behavioral Therapy for Insomnia (CBT-I)",
            "Medications (e.g., sleep aids)",
            "Sleep hygiene improvements"
        ],
        backgroundColor: "orange"
    }
};

// Function to populate a "select" field
function populateSelect(selectId, options) {
    const selectElement = document.getElementById(selectId);
    options.forEach(option => {
        const optionElement = document.createElement("option");
        optionElement.value = option;
        optionElement.textContent = option;
        selectElement.appendChild(optionElement);
    });
}

// Function to update the Result section
function updateResult(disorderType) {
    const resultBox = document.getElementById("disorder");
    const descriptionBox = document.getElementById("description");

    // Normalize disorderType to lower case to match keys
    const key = disorderType.toLowerCase();

    // Update disorder text (heading)
    resultBox.innerHTML = `<h4>${disorderType}</h4>`;

    // Update styling if disorder exists in disorderInfo
    if (key !== "-" && disorderInfo[key]) {
        resultBox.style.border = "none";
        resultBox.style.backgroundColor = disorderInfo[key].backgroundColor || "transparent";
        resultBox.style.color = "white";
    } else {
        // Reset styles for default
        resultBox.style.backgroundColor = "transparent";
        resultBox.style.color = "black";
        resultBox.style.border = "1px solid #ccc";
    }

    // Update description content
    const disorderData = disorderInfo[key];
    if (key !== "-" && disorderData) {
        descriptionBox.innerHTML = `
            <p id="descrip"><strong>Description:</strong><br> ${disorderData.description}</p>
            ${disorderData.causes ? `<p id="causes"><strong>Causes:</strong><ul>${disorderData.causes.map(cause => `<li>${cause}</li>`).join('')}</ul></p>` : ''}
            ${disorderData.treatment ? `<p id="treatment"><strong>Treatment:</strong><ul>${disorderData.treatment.map(treatment => `<li>${treatment}</li>`).join('')}</ul></p>` : ''}
        `;
    } else if (key == '-' && disorderData) {
        const disorder = document.getElementById("disorder");
        const disorderDescription = document.getElementById("description");
        const defaultKey = (Object.keys(disorderInfo))[0];
        disorder.innerHTML = `<h4>${defaultKey}</h4>`;
        disorderDescription.innerHTML = `<p>${disorderInfo[defaultKey.toLowerCase()].description}</p>`;
    } else {
        descriptionBox.innerHTML = "";
    }
}

// Form Submit handler with AJAX call to backend
const handleSubmission = (e) => {
    e.preventDefault();

    // 'this' inside an event listener is the form element
    // But since we're using an arrow function, 'this' is lexically scoped and not form
    // So better to explicitly get the form element:
    const form = e.target;

    // Collect all form values via FormData
    const formData = new FormData(form);

    // Convert FormData to plain object with keys matching backend expectations
    let formObject = {};
    formData.forEach((value, key) => {
        // Optional: convert dashes to underscores to match backend keys if needed
        formObject[key.replace(/-/g, '_')] = value;
    });

    // Send data to backend via AJAX (Fetch API)
    fetch("/predict", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formObject)
    })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not OK');
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                updateResult("-");
            } else {
                if (data.description) {
                    if (!disorderInfo[data.result.toLowerCase()]) {
                        disorderInfo[data.result.toLowerCase()] = {};
                    }
                    disorderInfo[data.result.toLowerCase()].description = data.description;
                }
                updateResult(data.result);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to get prediction from server.");
            updateResult("-");
        });
};


document.addEventListener("DOMContentLoaded", () => {
    // Populate select fields
    populateSelect("occupation", occupationOptions);
    populateSelect("gender", genderOptions);
    populateSelect("bmi", bmiOptions);

    // Load Default Result & Description
    const disorder = document.getElementById("disorder");
    const disorderDescription = document.getElementById("description");
    const defaultKey = (Object.keys(disorderInfo))[0];
    disorder.innerHTML = `<h4>${defaultKey}</h4>`;
    disorderDescription.innerHTML = `<p>${disorderInfo[defaultKey.toLowerCase()].description}</p>`;

    // Attach form submit event listener
    const form = document.querySelector("form");
    form.addEventListener("submit", handleSubmission);
});
