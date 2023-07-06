class MultiImportModal {
    constructor() {
        this.$modal = $("#import-process-modal");
        this.$modalBody = this.$modal.find('.modal-body');

        this.$formImport = document.getElementById('import-files');

        this.$btnClose = this.$modal.find('.btn-close');
        this.$btnImport = this.$modal.find('.btn-import');
    }

    show() {
        this.$modal.modal('show');
    }
}


class ImportChampionsDataModal extends MultiImportModal{
    constructor() {
        super();
        this.$modalBody.append(
            `
            <div class="mb-5">
                <label>Stats of champions</label>
                <input class="file file-block champions-stats-file" name="champions-stats-file" type="file" accept=".xlsx,.csv">
            </div>
            <div class="mb-5">
                <label>Class and roles of champions</label>
                <input class="file file-block champions-classes-roles-file" name="champions-classes-roles-file" type="file" accept=".xlsx,.csv">
            </div>
            `
        )
        this.$championsStatsFile = this.$modalBody.find('.champions-stats-file');
        this.$championsClassesRolesFile = this.$modalBody.find('.champions-classes-roles-file');

        this.$championsStatsFile.on('change', this.onChangeInput.bind(this));
        this.$championsClassesRolesFile.on('change', this.onChangeInput.bind(this));
    }

    onChangeInput() {
        const championsStatsFile = this.$championsStatsFile.val();
        const championsClassesRolesFile = this.$championsClassesRolesFile.val();

        if (!championsStatsFile || !championsClassesRolesFile ) return this.$btnImport.prop('disabled', true);

        this.$btnImport.prop('disabled', false);
    }



}
