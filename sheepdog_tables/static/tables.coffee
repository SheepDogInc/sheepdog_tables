class Columnn
    template_string: "<td><%= data =></td>" 

    template: () ->
        _.template(@template_string)

    render: (data) ->
        (do @template) data
