function isEmpty(obj,msg) //function to check empty field
{
	var len=obj.value.length;
	if(len==0)
	{
		alert("please enter " + msg);
		obj.focus();
		return false;
	}
	return true;
}
function isPassword(obj) //function to check password
{
	var pwdpattern=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
	if(obj.value.match(pwdpattern))
	{
		return true;
	}
	
	else
	{
		alert("Please Enter the password between 8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character");
		obj.focus();
		return false;
	}
}
function isAlphaNumaric(obj, minl,maxl)	//to check alphanumaric with min and max
	{
		var reg_Exp = /^[0-9a-zA-Z]+$/;		
		var obj_len = obj.value.length; 
		if(obj.value.match(reg_Exp)  && obj_len>=minl && obj_len<=maxl)	
			{
				return true;
			}
			else{
					alert("Please enter alphanumaric only and length between " +minl+ " and " +maxl);
					obj.focus();
					return false;
				}
	}
function isEmail(obj,msg) //function to check email
{
	var regex_email = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
	if(obj.value.match(regex_email))
	{
		return true;
	}
	else
	{
		alert("Please enter a valid "+msg);
		obj.focus();
		return false;
	}
}
function isSelect(obj,msg) //function to check select box
{
	if(obj.selectedIndex==0)
	{
		alert("Please Select the " + msg );
		return false;
	}
	else
	{
		return true;
	}
	
}
function isCheckBox(obj,msg) //function to check check box
{
    for (var i = 0; i < obj.length; i++) 
	{
        if (obj[i].checked) 
		{
            return true;
        }
    }
    alert("Please Select Your " + msg );
    return false;
}
function isFile(obj) //function to check picture file
{
	var val=obj.value;
	var FileExt = val.substr(val.lastIndexOf('.')+1);
	if ( FileExt != "jpg" && FileExt != "gif" && FileExt != "png")
	{
		alert("select only jpg, gif or png images:");
		obj.focus();
		return false;
	}
	else{
		return true;
	}
}
function isPhone(obj,minl, msg) //function to check phone number
	{
		var phoneno = /^(?:\+?91[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;		
		var obj_len = obj.value.length;
		
		if(obj.value.match(phoneno)&& obj_len>=minl)
		{
			return true;
		}
		else{
				alert(msg);
				obj.focus();
				return false;
			}
	}
