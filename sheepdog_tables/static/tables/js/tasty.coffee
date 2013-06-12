###
#   Tasty.coffee
#   These are utility classes to assist with handling tastypie data.
#   These are meant to be as generic as possible, but do expect that you are
#   working with tastypie.  Also, note you should have a table with the class
#   .ajax-table and a pagination div with the class .ajax-pager in order for
#   this to work as intended.
###
class TastyPager
    max_pages: 10
    gettext: (string) ->
        out = string
        if gettext?
            out = gettext(string)
        out

    template: _.template(
        "<ul>
        <li class='prev <% if (meta.previous === null) { %>disabled<% } %>'>
        <a href='javascript:void(0)'>#{ @gettext "Previous" }</a></li>
        <% for (var i = pageinfo.start; i < pageinfo.end; i++) { %>
            <li class='pages <% if (i === pageinfo.active) { %>active<% } %>'>
                <a id='page-<%= i %>' href='javascript:void(0)'><%= i + 1 %></a>
            </li>
        <% } %>
        <% if (pageinfo.end !== pageinfo.total) { %>
            <li class='active'><a href='javascript:void(0)'>...</a></li>
        <% } %>
        <li class='next <% if (meta.next === null) { %>disabled<% } %>'>
        <a href='javascript:void(0)'>#{ @gettext "Next" }</a></li>
        </ul>")

    get_pageinfo: (meta) ->
        pageinfo =
            total: Math.ceil(meta.total_count / meta.limit)
            active:  meta.offset / meta.limit 
            urls: {}

        start = 0
        end = pageinfo.total
        if pageinfo.total > @max_pages
            start = if pageinfo.active > 3 then pageinfo.active - 3 else 0
            end = Math.min(start + @max_pages, pageinfo.total)
            start = end - @max_pages if end - start < @max_pages


        base_url = meta.previous or meta.next
        return pageinfo if not base_url?

        for n in [start..end]
            url = $.param.querystring base_url, 
                offset: meta.limit * n
            pageinfo.urls[n] = url 

        pageinfo.start = start
        pageinfo.end = end
        pageinfo

    render: (meta, success) ->
        $pager = $ '.ajax-pager'
        $pager.show()

        pageinfo = @get_pageinfo meta
        $pager.hide() if pageinfo.start == pageinfo.end

        $pager.html @template
            meta: meta
            pageinfo: pageinfo

        # Hook up all our pager buttons
        if meta.next?
            $('.ajax-pager .next a').click () ->
                $.get meta.next, {}, success

        if meta.previous?
            $('.ajax-pager .prev a').click () ->
                $.get meta.previous, {}, success

        for page in $ '.ajax-pager .pages a'
            $page = $(page)
            if not $page.parent().hasClass('active')
                $page.click () ->
                    $.get pageinfo.urls[parseInt @.id.replace('page-', '')], {}, success


class TastyTableMixin
    table: null

    constructor: ->
        $thead = $ '.ajax-table thead'
        $thead.html "<tr></tr>"
        for header in @table.get_headers()
            $thead.append $ "<th>#{header}</th>" 

    render_table: (dataset) ->
        $tbody = $ '.ajax-table tbody'
        $tbody.html ""
        for object in dataset
            $row = $ '<tr></tr>' 
            for col in @table.table_sequence
                $row.append @table[col].render
                    data: object[col] or object
            $tbody.append $row
        @
    

Tables.Utils.namespace "Tables.Tasty", (exports) ->
    exports.TastyPager = TastyPager
    exports.TastyTableMixin = TastyTableMixin
