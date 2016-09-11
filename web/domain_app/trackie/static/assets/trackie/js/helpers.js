function renderFormErrors(element, error, keyPrefix) {
    element.find(".error").remove();

    for (var key in error){
        var list = $("<ul class='error'></ul>");
        for (var i=0; i < error[key].length; i++){
            list.append("<li>" + error[key][i] + "</li>");
        }
        var where = element.find("#" + keyPrefix + key);
        if (where.is("input")) {
            where.after(list);
        } else {
            where.append(list);
        }
    }
}