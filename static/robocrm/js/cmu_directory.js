$(document).ready(function(){
  $("#id_username").focusout(function(){
    var andrewID = $(this).val()

    var cmu = new CMUApi({
      id: "9c55f614-c85c-4fb9-b9db-5583351f606e",
      secret: "rtRPuoJZeGT5yiKQH6mFt9LZ1zMWFPb4z9olkJspfnPDygWukK_vjWuP"
    });

    var info = cmu.directory.findAndrewId(andrewID);

    if(info) {
      console.log(info);

      $("#id_first_name").val(info["first_name"]);
      $("#id_last_name").val(info["last_name"]);
      $("#id_email").val(info["email"]);
      $("#id_robouser-0-major").val(info["department"]);

      var year_offset = 0;

      switch(info["student_class"]) {
        case "Senior": {
          year_offset = 0;
          break;
        }
        case "Junior": {
          year_offset = 1;
          break;
        }
        case "Sophmore": {
          year_offset = 2;
          break;
        }
        case "Freshman": {
          year_offset = 3;
          break;
        }
      }

      var date = new Date();
      var current_year = date.getFullYear();
      // Spring if current month is less than June else new year
      var is_spring = (date.getMonth() < 5);

      if(!is_spring){
        //If in the Fall graduation is following year
        year_offset += 1;
      }

      var grad_year = current_year + year_offset;

      $("#id_robouser-0-grad_year").val(grad_year);


      var class_level = 1;

      if(info["student_level"] == "Undergrad") {
        class_level = 0;
      }

      $("#id_robouser-0-class_level>option:eq(" + class_level + ")").prop('selected', true);
    }
  });
});