$(function () {

    $('#backBtn').click(function () {
        // 窗口返回上一页面
        window.history.back()
    });
    $('#payBtnDiv > button').click(function () {
        $('#payMsg').text('使用' + $(this).text() + '正在支付');
        // $('#myModal').modal('show');
        // 弹出模态框，但不能点击内容以外关闭
        $('#myModal').modal({backdrop:'static', show:true});
        let orderNum = $(this).parent().attr('title');
        let payType = $(this).attr('title');
        $.getJSON('/app/pay/' + orderNum + '/' + payType, function (data) {
            if (data.status == 'ok') {
                $('#payMsg').text(data.msg);
                setTimeout(function () {
                    $('#myModal').modal('hide');
                    window.open('/app/cart', target = '_self');
                }, 3000)

            } else {
                $('#payMsg').text(data.msg);
            }
        });
    });
});
