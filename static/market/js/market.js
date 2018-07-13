$(function () {
    $('#allType').click(function () {
        // console.log('----1-----');
        $(this.lastChild).toggleClass('glyphicon-chevron-down');
        if ($('#typeDiv')[0].style.display == 'block') {
            $('#typeSortDiv').css('display', 'none');
            $('#typeDiv').css('display', 'none');
            return;
        }

        $('#typeSortDiv').css('display', 'block');
        $('#typeDiv').css('display', 'block');

        $('#goodsSort:last-child').removeClass('glyphicon-chevron-down');
        $('#sortDiv').css('display', 'none');

    });

    $('#goodsSort').click(function () {
        $(this.lastChild).toggleClass('glyphicon-chevron-down');

        if ($('#sortDiv')[0].style.display == 'block') {
            $('#typeSortDiv').css('display', 'none');
            $('#typeDiv').css('display', 'none');
            return;
        }
        $('#typeSortDiv').css('display', 'block');
        $('#sortDiv').css('display', 'block');


        $('#typeDiv').css('display', 'none');
        $('#allType:last-child').removeClass('glyphicon-chevron-down');


    });

    $('#typeSortDiv').click(function () {
        $(this).css('display', 'none');
        $('#sortDiv').css('display','none');
        $('#typeDiv').css('display','none');


        $('#allType:last-child').removeClass('glyphicon-chevron-down');
        $('#goodsSort:last-child').removeClass('glyphicon-chevron-down');

    })

    $('.addShopping').click(function () {
       let productid=$(this).attr('ga');
       $.getJSON('/app/addCart/'+productid,function (data) {

       })

    });

});







// $(function () {
//     $('#allType').click(function () {
//         console.log('---------');
//         $('#typeDiv').show('slow')
//
//     });
//
//
//
//
// });
 // $('#typeDiv').toggle("slow");