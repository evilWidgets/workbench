;; archive.el
;; name is wip.
;; manage auto-recover files, so they don't pollute target folders.

;; Let's ensure that the workbench/auto_recover_/ foler exists.
(let ((dir (expand-file-name "~/workbench_auto_recover/")))
  (unless (file-directory-p dir)
    (make-direcotry dir t))

  ;; 1. Auto-save files (named #foo#)
  (setq auto-save-file-name-transforms
	`((".*" ,(concat dir"/*\\1#") t)))

  ;; 2. Backup files (named foo~)
  (setq backup-directory-alist
	`((".*" . ,dir)))

  ;; 3. Auto-save-list files (Emacs' recovery metadata)
  (setq auto-save-list-file-prefix
	(concat dir "/auto-save-list/.saves-")))
