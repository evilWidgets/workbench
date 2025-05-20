;;; org-config.el --- Quiet Lighthouse Org Configuration

;; Set base directory
(setq org-directory "~/org")
(setq default-directory org-directory)

;; Ensure org-directory exists
(unless (file-directory-p org-directory)
  (make-directory org-directory))

;; Load Org
(require 'org)

;; Agenda setup
(setq org-agenda-files '("~/org/inbox.org"
                         "~/org/daily.org"
                         "~/org/projects.org"
                         "~/org/horizon.org"
			 "~/org/backlog.org" 
			 ))

(setq org-agenda-span 'week)
(global-set-key (kbd "C-c a") 'org-agenda)

;; Visuals (optional)
(setq org-hide-leading-stars t)
(setq org-startup-indented t)


;; Keybinding for capture
(global-set-key (kbd "C-c c") 'org-capture)
