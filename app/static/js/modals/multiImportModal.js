class MultiImportModal {
    constructor() {
        this.$modal = $("#import-process-modal");
        this.$modalBody = this.$modal.find('.modal-body');
        this.$modalFooter = this.$modal.find('.modal-footer');

        this.API = null;

        this.$formProcess = document.getElementById('upload-process-files');

        this.$dataFile = this.$modalBody.find('.data-file');
        this.$inforFile = this.$modalBody.find('.infor-file');
        this.$ignoreFile = this.$modalBody.find('.ignore-file');

        this.$btnClose = this.$modal.find('.btn-close');
        this.$btnProcess = this.$modal.find('.btn-process');

        this.$dataFile.on('change input', this.onChangeInput.bind(this));
        this.$inforFile.on('change input', this.onChangeInput.bind(this));
        this.$ignoreFile.on('change input', this.onChangeInput.bind(this));

        this.$btnProcess.on('click', this.onClickProcessBtn.bind(this));

    }

    show() {
        this.$modal.modal('show');
    }

    onChangeInput() {
        const dataFileName = this.$dataFile.val();
        const inforFileName = this.$inforFile.val();

        if (!dataFileName || !inforFileName ) return this.$btnProcess.prop('disabled', true);

        this.$btnProcess.prop('disabled', false);
    }
}
