function renderFormErrors(element, error, keyPrefix) {
    keyPrefix = keyPrefix ? keyPrefix : "";
    element.find(".error").remove();

    for (var key in error){
        var list = $("<ul class='error'></ul>");
        for (var i=0; i < error[key].length; i++){
            list.append("<li>" + error[key][i] + "</li>");
        }

        var where = (key === "id_non_field_errors") ? element.find("#" + key) : element.find("#" + keyPrefix + key);
        if (where.is("input")) {
            where.after(list);
        } else {
            where.append(list);
        }
    }
}

function slugify(text){
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '')
        .replace(/\-\-+/g, '-')
        .replace(/^-+/, '')
        .replace(/-+$/, '');
}