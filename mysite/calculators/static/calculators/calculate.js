$(document).ready(function () {

    $('#reizinasana_call').click(function () {
        reizini();
    })

    function reizini() {

        var e = document.getElementById("izvele");
        var strUser = e.options[e.selectedIndex].value;
        var input = document.getElementById("ievade").value;
        var products = ["/milk", "butter", "flour","/water","Honey"];
        var amount = [237, 250, 120,237,340];
        if (input > 0) {
            for (var x = 0; x < products.length; x++) {
                if (strUser == products[x])
                {
                    console.log(amount[x])
                    console.log(strUser);
                    var choice=products[x];
                    console.log("atrada");
                    if (choice[0]=="/"){
                        var sub=strUser.slice(1);
                        document.getElementById("Atbilde").innerHTML = input + " Cups of " + sub + " Converted to ml is " + input * amount[x] + "ml";
                    }
                    else{

                        document.getElementById("Atbilde").innerHTML = input + " Cups of " + strUser + " Converted to g is " + input * amount[x] + "g";
                    }
                }

            }

        }
        else {
            document.getElementById("Atbilde").innerHTML = "Conversion is not possible, the number is too small ";
        }

    }
});
