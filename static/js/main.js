var imagesobjinfo = {
	'__keyoftheelements__':function(){
		return "__kesnkjflsndfldnslenf__"; 
	},
	'getlist':function(){
		if(!imagesobjinfo[imagesobjinfo.__keyoftheelements__])
			return [];
		else
			return imagesobjinfo[imagesobjinfo.__keyoftheelements__];
	},
	'setlist':function(item){
		if(!imagesobjinfo[imagesobjinfo.__keyoftheelements__])
			imagesobjinfo[imagesobjinfo.__keyoftheelements__] = [];
		imagesobjinfo[imagesobjinfo.__keyoftheelements__].push(item);
	},
	'loadlist':function(listitems){
		if(!imagesobjinfo[imagesobjinfo.__keyoftheelements__])
			imagesobjinfo[imagesobjinfo.__keyoftheelements__] = [];
		imagesobjinfo[imagesobjinfo.__keyoftheelements__] = listitems;
	}
}

$(function(){
	var path = "/static/js/jsondata.json",
		localdata,
		parsed,
		callbackdata = function(data){
			localdata = data["listofimages"];
		};

	request_images_list(callbackdata).then(function(){
		imagesobjinfo.loadlist(localdata);
		renderimgs();
		var ownobserve = observeimgfolder(load_img);
	});
});

// Functions for random images
var request_images_list = function(callback){
	return $.ajax({
		url:"/static/js/jsondata.json",
		dataType: "json",
		cache:false,
		success:callback,
		error:function(err){
			console.warn(err);
		}
	})
}
var renderimgs = function(){
	var imgframe = $(".randomimages img");
	imgframe.attr("src","/static/imgs/glitched/" + imagesobjinfo.getlist()[0]);
	window.setTimeout(function(){
		var interval_load = window.setInterval(function(){
			var randn = Math.floor(Math.random() * imagesobjinfo.getlist().length);
			$(".randomimages img").attr("src","/static/imgs/glitched/" + imagesobjinfo.getlist()[randn]);
		},125);
	},5000);
}

// False-observer JS to folder
var load_img = function(){
	var list_imgs = [],
		callback_fn = function(data){
			list_imgs = data["listofimages"];
		};

	request_images_list(callback_fn).then(function(){
		if(list_imgs.length != imagesobjinfo.getlist().length){
			var difflistimg = _.difference(list_imgs,imagesobjinfo.getlist());
			for(j in difflistimg){
				imagesobjinfo.setlist(difflistimg[j]);
			}
		}
	});
}
var observeimgfolder = function(fn_suscriber,param){
	var observer = window.setInterval(function(){
		fn_suscriber(param);
	},1500);
	return observer;
}
var unsuscribeobserver = function(refobs){
	window.clearInterval(refobs);
}


