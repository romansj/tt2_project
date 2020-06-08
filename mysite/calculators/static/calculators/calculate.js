function reizini() {

    var e = document.getElementById("izvele");
    var strUser = e.options[e.selectedIndex].value;
    var input=document.getElementById("ievade").value;
    if (strUser=="milk"){
        var output=input*237;
        if (input<=0){
             document.getElementById("Atbilde").innerHTML="Conversion is not possible, the number is too small ";
        }
        else{
        document.getElementById("Atbilde").innerHTML=input+" Cups of "+strUser+" Converted to ml is "+output+"ml";
    }

    }
    else if (strUser=="butter-cups"){
        var output=input*250;
        if (input<=0){
             document.getElementById("Atbilde").innerHTML="Conversion is not possible, the number is too small ";
        }
        else{
        document.getElementById("Atbilde").innerHTML=input+" Cups of "+strUser+" Converted to g is "+output+"g";
    }
    }
    else if (strUser=="flour"){
        var output=input*120;
        if (input<=0){
             document.getElementById("Atbilde").innerHTML="Conversion is not possible, the number is too small ";
        }
        else{
        document.getElementById("Atbilde").innerHTML=input+" Cups of "+strUser+" Converted to g is "+output+"g";
    }
    }

}
