const RVDComment = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-textarea": primevue.textarea,
    },
    setup() {
        let comment = ref({comment: ''})
        return {comment}
    },
    mounted() {
        watch(this.comment, (comment, prevComment) => {
            this.setComment();
        });
        this.getComment();
        emitter.on('newOrder', e => this.getComment())
    },
    methods: {
        async getComment() {
            let resp = await get(API_COMMENT_GET)
            if (resp === undefined) {
                this.comment.comment = ''
            } else {
                this.comment.comment = resp
            }
            this.$forceUpdate();
        },
        async setComment() {
            let resp = await request(API_COMMENT_SET, {
                comment: this.comment.comment,
            })
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDComment).use(primevue.config.default).mount('#comment');
})