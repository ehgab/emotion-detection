let RunSentimentAnalysis = ()=>{
    textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            // Affiche la réponse QUEL QUE SOIT le status code
            let responseText = xhttp.responseText;
            try {
                let jsonResponse = JSON.parse(responseText);
                // Si c'est une erreur 400, affiche le message
                if (this.status == 400 && jsonResponse.message) {
                    document.getElementById("system_response").innerHTML = 
                        `<span style="color: red;">${jsonResponse.message}</span>`;
                } else if (this.status == 200 && jsonResponse.response) {
                    document.getElementById("system_response").innerHTML = jsonResponse.response;
                }
            } catch (e) {
                document.getElementById("system_response").innerHTML = responseText;
            }
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + textToAnalyze, true);
    xhttp.send();
} 