window.addEventListener('load', function() {
    setTimeout(function(){
        document.querySelectorAll('.alert-success').forEach(function(alert) {
            alert.style.transition = "opacity 0.5s ease-out";
            alert.style.opacity = "0";
            setTimeout(function(){
                alert.remove();
            }, 500);
        });
    }, 3000);
});