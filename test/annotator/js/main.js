var dire = "./ebola/";
var fileId = 5;
function upload(){
}
function goback(path){
	$("nav").fadeIn();
    $("article").fadeIn();
	$("article pre").hide();
	$("article pre").load(path+'.txt').fadeIn();
    $("#lemurbox").hide();
    $("#queuemode").attr("class","currentmode");
    $("#lemurmode").attr("class","switchmode");
	$("#docno").text("DOCNO: "+path+'.txt');
}

function topicAdd(){
	
}

$(document).ready(function(){		
	/*logout*/
	$("#logout").click(function(){document.cookie = "username=;"});	
	#("#topic_add").click(topicAdd)
	/*for Subtopic X,Y*/
	$(".edit").bind("click",edit);
	$(".confirmEdit").bind("click",confirmEdit);
	
	/*initial doc*/
	var path = dire + fileId+".txt";
	$("article pre").load(path);
	$("article").height(window.innerHeight-200).hide()
	$("#lemurbox").height(window.innerHeight-185)
	$("#docbox nav").hide()
	$("#lemurmode").attr("class","currentmode");
	$("#queuemode").attr("class","switchmode");
	
	$("#lemurmode").click(function(){
		$("nav").hide();
		$("article").hide();
		$("#lemurbox").fadeIn();
		$("#lemurmode").attr("class","currentmode");
		$("#queuemode").attr("class","switchmode");
	});
	$("#queuemode").click(function(){
		$("nav").fadeIn();
		$("article").fadeIn();
		$("#lemurbox").hide();
		$("#queuemode").attr("class","currentmode");
		$("#lemurmode").attr("class","switchmode");
	});
	
	$("#sidebar").height(window.innerHeight-5);
	$("#newDropbox").click(function(){$("#hint").hide(); $("#setDropbox").fadeIn();});
	$("#setup").click(newDropbox)
	$("#subtopicName").keypress(function (e){
		if (e.which == 13){
			e.preventDefault();
			newDropbox();
		}
	});
	$("#prev").click(prevDoc);
	$("#next").click(nextDoc);
});

function prevDoc(){
	if (fileId>1){
		fileId--;
		var path = dire + fileId+".txt";
		$("article pre").hide();
		$("article pre").load(path).fadeIn();
		$("#docno").text("DOCNO: "+path);
	}
	else {
		alert("already the first doc");
	}
}
function nextDoc(){
	if (fileId<10){
		fileId++;
		var path = dire + fileId+".txt";
		$("article pre").hide();
		$("article pre").load(path).fadeIn();
		$("#docno").text("DOCNO: "+path);
	}
	else {
		alert("already the last doc");
	}
}
/*
function inputKeypress(e){
	if (e.which == 13){
			e.preventDefault();
			confirmEdit();
	}
}
*/
function edit(){
	$(this).hide();
	$(this).siblings(".editbox").width(Math.max(200,$(this).siblings("h2").width())).val($(this).siblings("h2").text()).show()
	$(this).siblings(".confirmEdit").show();
	$(this).siblings("h2").hide();
}
function confirmEdit(){
	$(this).hide();
	$(this).siblings(".edit").show();
	$(this).siblings("h2").text($(this).siblings(".editbox").val()).show();
	$(this).siblings(".editbox").hide();
}
function createDropbox(){
	var $dropbox = $("<div></div>")
					.hide()
					.append($("<h2></h2>").text($("#subtopicName").val()))
					.append($("<input>").attr("class","editbox").hide())//.bind("keypress",inputKeypress))
					.append($("<div>edit</div>").attr({class:"edit"}).bind("click",edit))
					.append($("<div>confirm</div>").attr({class:"confirmEdit"}).bind("click",confirmEdit).hide())
					.append($("<div style='clear:both; padding-bottom:10px;'></div>"))
					.attr({class:"droppable",ondragover:"return false",ondrop:"annotate(event)",display:"none"});
	return $dropbox;
}
function newDropbox(){
	if ($("#subtopicName").val().trim() != ""){
		var $dropbox = createDropbox();
		$("#setDropbox").hide();
		$("#hint").fadeIn();
		$("#subtopicName").val("");
		$("#dropboxList").prepend($dropbox.fadeIn());	
	}
	else{
		alert("Invalid subtopic name");
	}
}
function newAnnotate(event){
	var form,score,removeImg,add,docinfo;
	add = document.createElement("div");
	add.setAttribute("class","annotating");
	add.innerHTML = event.dataTransfer.getData("text/plain");
	docinfo = document.createElement("div");
	docinfo.innerHTML = "From DOC: "+dire + fileId+".txt";
	docinfo.setAttribute("class","docinfo");
	docinfo.fileid = fileId;
	docinfo.addEventListener("click",function(){goback(dire+this.fileid);});
	add.appendChild(docinfo);
	form = document.createElement("form");
	for (i=1;i<=4;i++){
		score = document.createElement("input");
		score.type = "radio";
		score.name = "score";
		score.setAttribute("class","eval")
		score.value = i;
		scoreText = document.createTextNode(i);
		form.appendChild(scoreText);
		form.appendChild(score);
	}
	removeImg = document.createElement("img");
	removeImg.setAttribute("src","./img/trash.png");
	removeImg.setAttribute("class","remove");
	removeImg.addEventListener("click",removeAnnotated);
	form.appendChild(removeImg);
	add.appendChild(form);
	return add;
}
function annotate(event){
	var $dropbox,add,dropbox;
	event.preventDefault();
	add = newAnnotate(event);

	$dropbox = $(event.target);
	dropbox = event.target;
	while ($dropbox.attr("class")!="droppable"){
		$dropbox = $dropbox.parent();
		dropbox = dropbox.parentNode;
	}	
	lastAnnotated = $dropbox.children(".annotating").last();
	if (lastAnnotated != null){
		lastAnnotated.attr({class:"annotated"});		
	}
	$(add).appendTo($dropbox).hide().fadeIn(300);
	dropbox.scrollTop = dropbox.scrollHeight;
}

function removeAnnotated(event){
	$(event.target).parent().parent().fadeOut(300);
	setTimeout(function(){$(event.target).parent().parent().remove()},300);
}


function snapSelectionToWord() {
	rangy.getSelection().expand("word");
}

/*more: 
	input check
	colorful button	
	confirm	
	drag drop catch error
	subtopicName no scroll
*/
