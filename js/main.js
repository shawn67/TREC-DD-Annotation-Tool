var dire = "./ebola/";
var delete_passage = []

function view(){
	$.post("./view.cgi",{"topic_name" : $("#topic_selection option:selected").val()}, function(retData) {$("body").append("<iframe src='" + document.getElementById("username").innerHTML+ ".csv" + "' style='display: none;' ></iframe>");}); 
}

function upload(){
	var json_pack = {subtopics:[]}
	json_pack.topic_name = $("#topic_selection option:selected").val();
	json_pack.state = state;
	json_pack.browseposition = fileId;
	subtopics = document.getElementsByClassName("droppable");
	for (var i = 0; i < subtopics.length; i++){
		var subtopic = new Object();
		json_pack.subtopics.push(subtopic);
		subtopic.subtopic_name = subtopics[i].getElementsByTagName("h2")[0].innerHTML
		subtopic.passages = []
		subtopic.position = $(subtopics[i]).scrollTop();
		var passages = subtopics[i].getElementsByClassName("passage");
		for (var j = 0; j < passages.length; j++){
			var passage = new Object();
			passage.passage_name = passages[j].getElementsByTagName("p")[0].innerHTML;
			passage.url = passages[j].getElementsByTagName("a")[0].innerHTML;
			passage.offset_start = passages[j].offset_start;
			passage.offset_end = passages[j].offset_end;
			if (passages[j].getElementsByClassName("passage_id").length > 0){
				passage.passage_id = passages[j].getElementsByClassName("passage_id")[0].innerHTML;
			}
			evaluation = passages[j].getElementsByTagName("input");
			for (var k = 0; k < 4; k++){
				if (evaluation[k].checked){
					passage.grade = k + 1;
				}
			}
			subtopic.passages.push(passage);
		}
	}
	json_pack.delete_passage = delete_passage;
	//alert(JSON.stringify(json_pack));
	$.post("./data.cgi",{"data" : JSON.stringify(json_pack)},function(){alert("save completed"); location.reload();});
}	

function topicAdd(){
	$("#addtopic").fadeIn();
	//$(this).hide();
}

function topicEdit(){
	$("#confirm_topic input").val($("#topic_selection option:selected").val());
	$("#confirm_topic").fadeIn();
	original_topic_name = $("#topic_selection option:selected").val();
}

function addTopic(){
	if ($("#addtopic input").val().trim() != ""){
		newtopic = $("#addtopic input").val();
		$("#topic_selection").append($("<option></option>").text(newtopic).val(newtopic));
		$.post("./newtopic.cgi",{"topic_name": newtopic, "domain_name" :$("#change_domain option:selected").val()})
		$("#addtopic input").val("");
	}
	$("#addtopic").hide();	
}

function confirmTopic(){
	new_topic_name = $("#confirm_topic input").val();
	$("#topic_selection option:selected").val(new_topic_name);
	$("#topic_selection option:selected").text(new_topic_name);
	$.post("./newtopic.cgi",{"topic_name": original_topic_name, "new_topic_name": new_topic_name});
	$("#confirm_topic").hide();
}

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

function goback(path){
	$("nav").fadeIn();
    $("article").fadeIn();
	$("article pre").hide();
	$("article pre").load(path).fadeIn();
    $("#lemurbox").hide();
    $("#queuemode").attr("class","currentmode");
    $("#lemurmode").attr("class","switchmode");
	$("#docno").text("DOCNO: "+path);
	fileId = path.match(/\d+/);
}

$(document).ready(function(){
	/*init*/
	fileId = document.getElementById("fileId").innerHTML;
	$(".droppable").each(function(){
		$(this).scrollTop($(this).find("span").text());
	});
	var path = dire + fileId+".txt";
	$("#docno").text("DOCNO: "+path);
	/*logout*/
	$("#logout").click(function(){document.cookie = "username=;"});	
	$("#topic_add").click(topicAdd);
	$("#topic_edit").click(topicEdit);
	
	/*bind event*/
	$(".edit").click(edit);
	$(".confirmEdit").click(confirmEdit);
	$(".remove").click(removeAnnotated);
	$("#addtopic img").click(addTopic);
	$("#addtopic input").keypress(function (e){
		if (e.which == 13){
			e.preventDefault();
			addTopic();
		}
	});
	
	$("#confirm_topic img").click(confirmTopic);
	$("#confirm_topic input").keypress(function (e){
		if (e.which == 13){
			e.preventDefault();
			confirmTopic();
		}
	});
	/*initial doc*/
	var path = dire + fileId+".txt";
	$("article pre").load(path);
	$("article").height(window.innerHeight-210);
	$("#lemurbox").height(window.innerHeight-171)
	if (document.getElementById("state").innerHTML=="1"){
		$("#lemurmode").attr("class","currentmode");
		$("#queuemode").attr("class","switchmode");
		$("article").hide();
		$("nav").hide();
		state = 1;
	}else{
		$("#lemurmode").attr("class","switchmode");
		$("#queuemode").attr("class","currentmode");
		$("#lemurbox").hide();
		state = 0;
	} 
		
	
	$("#lemurmode").click(function(){
		$("nav").hide();
		$("article").hide();
		$("#lemurbox").fadeIn();
		$("#lemurmode").attr("class","currentmode");
		$("#queuemode").attr("class","switchmode");
		state = 1;
	});
	$("#queuemode").click(function(){
		$("nav").fadeIn();
		$("article").fadeIn();
		$("#lemurbox").hide();
		$("#queuemode").attr("class","currentmode");
		$("#lemurmode").attr("class","switchmode");
		state = 0;
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
function newAnnotate(event, offset_start, offset_end){
	var form,score,removeImg,add,docinfo;
	add = document.createElement("div");
	add.setAttribute("class","annotating");
	$(add).addClass("passage");
	wrap = document.createElement("p")
	wrap.innerHTML = event.dataTransfer.getData("text/plain");
	add.appendChild(wrap);
	add.offset_start = offset_start;
	add.offset_end = offset_end;
	docinfo = document.createElement("div");
	docinfo.innerHTML = "From DOC: <a>"+dire + fileId+".txt</a>";
	docinfo.setAttribute("class","docinfo");
	docinfo.fileid = fileId;
	docinfo.addEventListener("click",function(){goback(dire+this.fileid+".txt");});
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
	selection = window.getSelection();
	offset_start = selection.anchorOffset;
	offset_end = offset_start + selection.toString().length;
	event.preventDefault();
	add = newAnnotate(event, offset_start, offset_end);

	$dropbox = $(event.target);
	dropbox = event.target;
	while ($dropbox.attr("class")!="droppable"){
		$dropbox = $dropbox.parent();
		dropbox = dropbox.parentNode;
	}	
	lastAnnotated = $dropbox.children(".annotating").last();
	if (lastAnnotated != null){
		lastAnnotated.removeClass("annotating").addClass("annotated");	
	}
	$(add).appendTo($dropbox).hide().fadeIn(300);
	dropbox.scrollTop = dropbox.scrollHeight;
}

function removeAnnotated(event){
	$passage = $(event.target).parent().parent()
	$passage.fadeOut(300);
	if ($passage.children(".passage_id").length > 0) {
		delete_passage.push($passage.children(".passage_id").text())
	}
	setTimeout(function(){$passage.remove()},300);
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
