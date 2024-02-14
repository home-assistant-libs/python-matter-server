import type { TemplateResult } from "lit";

interface BaseDialogBoxParams {
  confirmText?: string;
  text: string | TemplateResult;
  title: string;
}

export interface PromptDialogBoxParams extends BaseDialogBoxParams {
  cancelText?: string;
}

function dialogHelper(
  element: HTMLElement,
  type: "alert" | "prompt",
  dialogParams: PromptDialogBoxParams
) {
  import("./dialog-box");
  return new Promise<boolean>((resolve) => {
    const dialog = document.createElement("dialox-box");
    dialog.params = dialogParams;
    dialog.dialogResult = resolve;
    dialog.type = type;
    document.body.appendChild(dialog);
  });
}

export const showAlertDialog = (
  element: HTMLElement,
  dialogParams: BaseDialogBoxParams
) => dialogHelper(element, "alert", dialogParams);

export const showPromptDialog = (
  element: HTMLElement,
  dialogParams: BaseDialogBoxParams
) => dialogHelper(element, "prompt", dialogParams);
