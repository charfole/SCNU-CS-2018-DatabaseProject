// last.html 的js 逻辑

console.log("ok");
$(".delete").click(function() {
    console.log(this.attr("data-id"));
})

// $('.wrap').on('click', '.delete', function() {
//     console.log(this);
// })