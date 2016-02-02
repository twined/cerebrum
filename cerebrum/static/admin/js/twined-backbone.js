/* backbone */

//TODO: fix header slug generation when receiving pasted material.

var app = app || {};
    app.vent = app.vent || _.extend({}, Backbone.Events);
    app.Posts = app.Posts || {};

    app.Posts.MainView = Backbone.View.extend({
        el: 'body',
        events: {
            'submit form': 'clickSubmit'
        },

        initialize: function() {
            that = this;
            this.isDirty = false;
            app.vent.on('posts:change', this.markDirty, this);
            window.onbeforeunload = function() {
                if (that.isDirty) {
                    return 'Du har foretatt endringer på denne siden ' +
                           'uten å lagre disse. Ved å navigere bort ' +
                           'vil disse endringene gå tapt.';
                }
            };
        },

        clickSubmit: function(e) {
            app.vent.trigger('posts:submit', e);
            form = this.checkForm();
            if (form['valid'] === false) {
                e.preventDefault();
            }
            window.onbeforeunload = $.noop();
        },

        checkForm: function() {
            var form = {
                'valid': true,
                'errors': []
            };
            if ($titleEl.val() === '') {
                form['errors'].push('Overskrift kan ikke være blank.');
                form['valid'] = false;
                $titleEl.parent().parent().addClass('error');
                $titleEl.parent().parent().append('<span class="help-inline"><strong><i class="icon-hand-up"></i> Feltet er påkrevet.</strong></span>');
                $('html, body').animate({
                    scrollTop: 0
                }, 5);
            }
            // clean body text here?
            return form;
        },

        markDirty: function() {
            this.isDirty = true;
        }
    }),

    /* not implemented yet */
    app.Posts.KeywordsView = Backbone.View.extend({
        el: '#btnGetKeywords',
        keywordsEl: '#id_meta_keywords',
        sourceEl: '#id_body',
        buttonEl: '#btnGetKeywords',
        url: 'get-keywords/',

        events: {
            'click': 'getKeywords'
        },

        initialize: function() {

        },

        getKeywords: function(e) {
            $.get(
                this.url,
                {text: $(this.sourceEl).val()},
                function(result) {
                    $('#id_meta_keywords').text(result['keywords']);
            });
            e.preventDefault();
        }
    }),

    app.Posts.LeadView = Backbone.View.extend({
        events: {
            'keydown': 'change',
            'keyup': 'change'
        },

        initialize: function(options) {
            this.$el = options.lead;
        },

        change: function(e) {
            app.vent.trigger('posts:lead:change');
            app.vent.trigger('posts:change');
        }
    }),

    app.Posts.HeaderView = Backbone.View.extend({
        statusEl: '.slug-status',
        url: 'check-slug/',

        events: {
            'blur': 'change',
        },

        initialize: function(options) {
            this.$el = options.header;
            this.$statusEl = $(this.statusEl);
            this.$slugEl = options.slug;
            this.$el.slugIt({
                output: this.$slugEl,
                map: { 'æ': 'ae', 'ø': 'oe', 'å': 'aa', '\'': '' },
                space: '-'
            });
            app.vent.on('posts:header:change', this.checkSlug, this);
        },

        checkSlug: function() {
            that = this;
            slug = this.$slugEl.val();

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                type: 'GET',
                url: this.url,
                data: {'slug': slug},
                success: function(data) {that.onSuccess(data, that);},
                dataType: 'json'
            });
        },

        onSuccess: function(data, that) {
            if (data.status == 200) {
                app.vent.trigger('posts:header:success', data);
                that.slugSuccess(data);
            } else if (data.status == 400) {
                app.vent.trigger('posts:header:error', data);
                that.slugError(data);

            }
        },

        showTooltip: function(title) {
            this.$slugEl.tooltip({
                'title': title,
                'trigger': 'manual',
                'placement': 'bottom'
            });
            this.$slugEl.tooltip('show');
        },

        hideTooltip: function() {
            this.$slugEl.tooltip('destroy');
        },

        slugError: function(data) {
            this.$slugEl.parent().parent().removeClass('has-success');
            this.$slugEl.parent().parent().addClass('has-error');
            this.showTooltip('Ugyldig slug.');
            this.disableSubmitButton();
        },

        slugSuccess: function(data) {
            this.$slugEl.parent().parent().removeClass('has-error');
            this.$slugEl.parent().parent().addClass('has-success');
            this.$slugEl.val(data.slug);
            this.hideTooltip();
            this.enableSubmitButton();
        },

        disableSubmitButton: function() {
            $("input[type=submit]").attr('disabled', 'disabled');
            $("input[type=submit]").removeClass('btn-primary').addClass('btn-error');

        },

        enableSubmitButton: function() {
            $("input[type=submit]").removeAttr("disabled");
            $("input[type=submit]").removeClass('btn-error').addClass('btn-primary');
        },

        change: function(e) {
            app.vent.trigger('posts:header:change');
            app.vent.trigger('posts:change');
        }
    }),

    app.Posts.ToggleTemplateLockView = Backbone.View.extend({
        el: '#toggleTemplateLock',
        sourceEl: '#id_body',

        locked: true,

        events: {
            'click': 'toggleTemplateLock'
        },

        initialize: function() {
            this.$sourceEl = $(this.sourceEl);
            //this.$content = $(this.$sourceEl.html());
            this.$content = this.getHTML();
            this.setAllEditable(this.$content);
            this.lockTemplate(this.$content);
            app.vent.on('posts:submit', this.clean, this);
        },

        getHTML: function() {
            return $(this.$sourceEl.editable("getHTML"));
        },

        setHTML: function(html) {
            return $(this.$sourceEl.editable("setHTML", html));
        },

        clean: function(e) {
            $content = this.getHTML();
            if ($content.attr('contenteditable')) {
                $content.removeAttr('contenteditable');
            }
            $content.find('*').each(function() {
                console.log('clean $content.each = ' + $(this).html());
                if ($(this).attr('contenteditable')) {
                    $(this).removeAttr('contenteditable');
                }
            });
            wrappedContent = $('<div>').append($content.clone()).html();
            this.setHTML(wrappedContent);
        },
        setAllEditable: function($content) {
            $content.attr('contenteditable', 'true');
            $content.find('*').each(function() {
                $(this).attr('contenteditable', 'true');
            });
            wrappedContent = $('<div>').append($content.clone()).html();
            this.setHTML(wrappedContent);
        },

        lockTemplate: function($content) {
            if ($content.hasClass('.locked')) {
                $content.attr('contenteditable', 'false');
            }
            $content.find('.locked').each(function() {
                $(this).attr('contenteditable', 'false');
            });
            this.locked = true;
            wrappedContent = $('<div>').append($content.clone()).html();
            this.setHTML(wrappedContent);
        },

        unlockTemplate: function($content) {
            if ($content.hasClass('.locked')) {
                $content.attr('contenteditable', 'true');
            }
            $content.find('.locked').each(function() {
                $(this).attr('contenteditable', 'true');
                console.log('lock: ' + $(this).prop('tagName') + ' ' + $(this).attr('class'));
            });
            this.locked = false;
            console.log('Template is unlocked!');
            wrappedContent = $('<div>').append($content.clone()).html();
            this.setHTML(wrappedContent);
        },

        toggleTemplateLock: function(e) {
            if (this.locked) {
                this.unlockTemplate(this.$content);
                this.$el.html('<i class="fa fa-lock"> </i> Lås mal');

            } else {
                this.lockTemplate(this.$content);
                this.$el.html('<i class="fa fa-lock"> </i> Lås opp mal');
            }
            e.preventDefault();
        }
    });