const transformButton = document.getElementById("transformButton");
const algorithmSelectBox = document.getElementById("algorithmSelectBox");
const sourceTextArea = document.getElementById("sourceTextArea");
const outputTextArea = document.getElementById("outputTextArea");
const postUrl = document.getElementById("postUrl").innerText;

let selectedAlgorithmText = "";
let selectedAlgorithmValue ="";

function MakeSumarry(e) {
    var model = {
        "SourceText": sourceTextArea.value,
        "AlgorithmTypeValue": selectedAlgorithmValue
    };
    
    $.ajax({
        type: "POST",
        url:  postUrl,
        data: {SourceText:model.SourceText,AlgorithmTypeValue: model.AlgorithmTypeValue},
        success: function(result) {
            outputTextArea.value = result.sourceText;
        },
        error: function(xhr, status, error) {
            console.log("hata");
        }
    });
}

$(algorithmSelectBox).change(function () {
    var opt = $(this).find(':selected');
    selectedAlgorithmText = opt.text();
    selectedAlgorithmValue = opt.val();
});

$(document).ready(function() {
    transformButton.addEventListener("click",MakeSumarry);
});