const dataset = "Sleep Dataset";
const datasetDescription = "Downloaded from <i>Kaggle</i>.<br>Has 3 output class:<br><i>No Disorder, Sleep Apnea & Insomnia.</i><br>Has 373 data, 12 features and 1 target.";
const modelName = "Logistic Regression";
const metrics = "Accuracy: 94%<br/>Precision: 50%";


const dataset_image = {
    "img_name": "Bar Chart",
    "url": "/static/assets/bar_chart.png",
    "alternative": "Bar_Chart"
}

const model_image = {
    "img_name": "Line Chart",
    "url": "/static/assets/line_chart.png",
    "alternative": "Line_Chart"
}

document.addEventListener("DOMContentLoaded", () => {
    const datasetName = document.getElementById("datasetName");
    const datasetDesc = document.getElementById("datasetDesc");
    const model = document.getElementById("model-name");
    const evaluationMetrics = document.getElementById("metrics-desc");

    datasetName.innerHTML = dataset;
    datasetDesc.innerHTML = datasetDescription;
    model.innerHTML = modelName;
    evaluationMetrics.innerHTML = metrics;

    const datasetImg = document.querySelector("#dataset-img img");
    const datasetImgName = document.getElementById("dataset-graph-name");
    const modelImg = document.querySelector("#model-img img");
    const modelImgName = document.getElementById("model-graph-name")

    datasetImgName.innerHTML = dataset_image.img_name;
    datasetImg.src = dataset_image.url;
    datasetImg.alt = dataset_image.alternative

    modelImgName.innerHTML = model_image.img_name;
    modelImg.src = model_image.url;
    modelImg.alt = model_image.alternative;
});