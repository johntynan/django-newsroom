<script type="text/javascript" src="{{MEDIA_URL}}js/swfobject.js"></script>
<script type="text/javascript">

function sendEvent(swf,typ,prm) { 
  thisMovie(swf).sendEvent(typ,prm); 
};
function getUpdate(typ,pr1,pr2,swf) {
  //if(typ == 'state') { alert('the current state is: '+pr1); }
};
function thisMovie(swf) {
  if(navigator.appName.indexOf("Microsoft") != -1) {
    return window[swf];
  } else {
    return document[swf];
  }
};

//jw player
var player = "{{MEDIA_URL}}swf/player.swf"; 

//jw player
var flashvars = {
  file: "http://youtube.com/watch%3Fv%3D{{object.video_id}}",
  //fallback: "{{MEDIA_URL}}{{object.video_flv}}",
  searchbar:false,
  image: "{{object.thumbnail_url}}",
  shownavigation: false,
  bgcolor: "#000",
  //autoPlay: true,
  width: "480",
  height: "360",
  javascriptid: 'videocontent',
  enablejs: true,
};

var params = {};

var attributes = {
  id: "videocontent",
  name: "videoplayer"
};    

swfobject.embedSWF(
    player,
    "videocontent", 
    '480',//"{{object.get_frame_width}}", 
    '360',//"{{object.get_frame_height}}", 
    "8",
    "", //"{{MEDIA_URL}}swf/expressInstall.swf", 
    flashvars, params, attributes);
</script>
