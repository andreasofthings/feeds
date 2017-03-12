$('.feeds-tooltip').tooltip();

//Get the context of the canvas element we want to select
var ctx = $("#chart").get(0).getContext("2d");
var myChart = new Chart(ctx).Line(data);

//$(function () {
//    $('.refresh form a').on('click', function (e) {
//        e.preventDefault();
//        $(this).parent('form').submit();
//    });
//});
