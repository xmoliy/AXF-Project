$(function () {
    topSwiper();
    topSwiper2();
    
});

function  topSwiper() {
    let swiper = Swiper("#topSwiper",{
        direction: "horizontal",
        loop: true,
         // 如果需要分页器
        pagination: '.swiper-pagination',
        effect : 'fade',
        paginationClickable :true,
        autoplay:1,
        autoplayDisableOnInteraction : false,

    })
}
function topSwiper2() {
    let swoper2 = new Swiper('#swiperMenu',{
        direction:"horizontal",
        slidesPerView:3,
        spaceBetween:5,
        loop:false,
    });

};