$(function () {
//    是否选择购买的span添加点击时间
    $('.isChose').click(function () {
        var spanChild = $(this).children().first();
        id = spanChild.attr('id');
        if (spanChild.text().trim() == '') {
            spanChild.text('√');
            // console.log('选择' + id);
        } else {
            spanChild.text('');
            // console.log('取消' + id);
        }
        checkAllChose();
        $.getJSON('/app/select/' + id, function (data) {
            console.log(data);
            if (data.status == 200) {
                //购物车总价格Element
                var tp = $('#totalPrice').text().trim();
                console.log('totalPrice' + tp);
                if (data.selected) {
                    //    选择
                    $('#totalPrice').text((parseFloat(tp) + parseFloat(data.price)))
                } else {
                    //取消选择
                    $('#totalPrice').text((parseFloat(tp) - parseFloat(data.price)))
                }
            }
        });

    });
    $('#allChose').click(function () {
        let span = $(this).children().first();
        let id = 0;
        if (span.text().trim() == '') {
            span.text('√');
            $('.isChose :first-child').text('√');
            id = 0;

        } else {
            span.text('');
            $('.isChose :first-child').text('');
            id = 99999
        }
        //更新后台
        $.getJSON('/app/select/' + id, function (data) {
            $('#totalPrice').text(data.price)
        });


    });


    $('.subShopping').click(function () {
        cnt = $(this).next();
        if (parseInt(cnt.text()) > 0) {
            cnt.text(parseInt(cnt.text()) - 1)
        }
         let tp = $('#totalPrice').text().trim();
         $.getJSON('/app/subCart/'+$(this).next().attr('id'),function (data) {
             $('#totalPrice').text((parseFloat(tp) - parseFloat(data.price)))


            })
    });

    $('.addShopping').click(function () {
        cnt = $(this).prev();
        cnt.text(parseInt(cnt.text()) + 1);
        let tp = $('#totalPrice').text().trim();
        $.getJSON('/app/addCart/'+$(this).prev().attr('id'),function (data) {
             $('#totalPrice').text((parseFloat(tp) + parseFloat(data.price)))
        })

    });
    checkAllChose()
     $('#toOrder').click(function () {
        window.open('/app/order/0',target='_self');
    })
});
function checkAllChose() {
    let choose=$('.isChose');
    for (let i=0;i<choose.length;i++){
        if($(choose[i]).children().first().text().trim()==''){
            $('#allChose :first-child').text();
            return;
        }
    }
    $('#allChose :first-child').text('√');
}
