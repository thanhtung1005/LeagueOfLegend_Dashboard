class ShowTableModal {
    constructor() {
        this.$modal = $('#show-table-modal');
        this.$modalBody = this.$modal.find('.modal-body')
        this.$btnExport = this.$modal.find('.btn-export');
        this.$countResult = this.$modal.find('.count-result-info');
        this.$resultList = this.$modal.find('.body-table-modal');
        this.$headerTable = this.$modal.find('.header-table-modal tr');
        this.$title = this.$modal.find('.modal-title');
        this.$desc = this.$modal.find('.modal-desc');

        this.$btnExport.on("click", this.onClickBtnExport.bind(this));
    }

    show(title, data, desc, btnExportCallback) {
        this.$title.text(title || '');

        this.options = data.options || {};

        this.tableHeader = data.header || [];
        this.tableData = data.data || [];

        this.$desc.text(desc || '');

        this.btnExportCallback = btnExportCallback;
        if (!this.btnExportCallback) this.$btnExport.addClass('d-none');
        else this.$btnExport.removeClass('d-none');

        this.$countResult.addClass('d-none').empty();
        if (this.options.countResult) {
            this.$countResult.removeClass('d-none').html(`
                <span class="mr-3">Successfully: <span class="text-success font-weight-semibold">${this.options.countResult.success || 0}</span></span>
                <span class="mr-3">Error: <span class="text-danger font-weight-semibold">${this.options.countResult.error || 0}</span></span>
            `)
        }
        this.renderResultList();
        this.$modal.modal("show");
    }

    renderResultList() {
        this.$headerTable.empty();
        for (let i = 0; i < this.tableHeader.length; i++) {
            this.$headerTable.append(`<th>${this.tableHeader[i]}</th>`);
        }
        this.$resultList.empty();
        let length = this.tableData.length;
        if (length === 0) return this.$resultList.append(`
            <tr>
                <td colspan="99" class="text-center">Empty</td>
            </tr>
        `);
        for (let i = 0; i < length; i++) {
            let row = this.tableData[i];
            let $tr = $('<tr></tr>');
            for (const col of row) {
                $tr.append(`<td>${(col === 0 || col)? col : ''}</td>`)
            }
            this.$resultList.append($tr);
        }
    }

    async onClickBtnExport() {
        this.btnExportCallback && await this.btnExportCallback(this.tableHeader, this.tableData);
    }
}
