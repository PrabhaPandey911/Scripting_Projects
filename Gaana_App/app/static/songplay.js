$(document).ready(function() {
   
    $('img[name=songs]').on('click',function(e){
      path=$(this).data('link');
      img=$(this).data('image');
      name=$(this).data('name');
      data_send=$(this).data('sid');

     $('#bottom-nav').css("display","block");
     $('#audio-player').attr("src",path);
     $('#audio-player').attr("preload",'true');
     $('#audio-player').attr("autoplay",'true');
     $('#song-name-preview').text(name);
     $('.cover').attr('src',img);
     $('.cover').attr('width','110');
     $('.cover').attr('height','114');
     $('.mejs-horizontal-volume-current').css('width','80px');
     $('.mejs-horizontal-volume-handle').css('left','74px');
     id=$(this).data('id');      
  
     $.ajax({
          type: "POST",
          url: "/recent/"+id,
          // data: id,
          success: function (result) {
              console.log("success");
          },
          error: function (e) {
              console.log("ERROR : ", e);
          }
                
          });

    $.getJSON('/songsjson/'+data_send,function(data) {

            array=data
           
            var i;
        for (i = 0; i < array.length; i++) {
            if(array[i][2]==path)
            indx=i;
        } 

    });
    });
    $bar = $('#block_content');
  
  
         $('a').click(function(e){
          e.preventDefault();
          // console.log("hi");
          var url=$(this).attr('href');
          // console.log(url);
          $('#block_content').load(url);
          // localStorage.setItem('display', $bar.html());
  
        });
      
   });