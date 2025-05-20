;;; capture.el --- WorkBench capture templates -*- lexical-binding: t; -*-

(require 'org)
(require 'org-id)

(defconst wb/org-inbox-file    "~/workbench/org/inbox.org")
(defconst wb/org-projects-file "~/workbench/org/projects.org")

(setq org-capture-templates
      `(

        ;;✅ Inbox
        ("i" "Inbox" entry
         (file+headline ,wb/org-inbox-file "Inbox")
         ,(concat
           "* TODO %^{Title}\n"
           ":PROPERTIES:\n"
           ":CREATED:        %U\n"
           ":SCHEDULED:      %^{Scheduled}t\n"
           ":DEADLINE:       %^{Deadline}t\n"
           ":CLOSED_TASK:    %^{Yes|No}\n"
           ":STATUS:         %^{Status|TODO|DOING|DONE|WAITING_FOR|CANCELLED}\n"
           ":PRIORITY:       %^{Priority|A|B|C|D}\n"
           ":CATEGORY:       %^{Category}\n"
           ":TAGS:           %^{Tags}\n"
           ":STAKEHOLDER_WEIGHT: %^{Stakeholder Weight (3=Critical, 2=Moderate, 1=Minimal)|3|2|1}\n"
           ":REF:            %a\n"
           ":SOURCE:         %^{Source|manual|web|module|email|api}\n"
           ":ORIGIN:         inbox.org\n"
           ":CAPTURE_ID:     %(org-id-uuid)\n"
           ":TYPE:           %^{Type|task|note|question|log|event|memo}\n"
           ":CONFIDENCE:     0.5\n"
           ":LABEL_HASH:     %(substring (md5 (format-time-string \"%Y%m%d%H%M%S\")) 0 4)\n"
           ":END:\n"
           "%i\n"
           "%?"))

        ;;✅ Project
        ("p" "Project" entry
         (file+headline ,wb/org-projects-file "Projects")
         ,(concat
           "* PROJECT %^{Project Title}\n"
           ":PROPERTIES:\n"
           ":CREATED:          %U\n"
           ":ID:               %(org-id-new)\n"
           ":Number_of_Tasks:  %^{Number of Tasks|auto}\n"
           ":Effort_Estimate:  %^{Effort Estimate|auto}\n"
           ":END:\n"
           "%?") 
         :immediate-finish t)

        ;;✅ Generic Task (auto-sort into projects)
        ("t" "Task" entry
         (file+headline ,wb/org-inbox-file "Inbox")
         ,(concat
           "* TODO %^{Title}\n"
           ":PROPERTIES:\n"
           ":CREATED:   %U\n"
           ":END:\n"
           "%?\n"
           "%(shell-command-to-string \"~/workbench/tools/post_sort_inbox.py --projects\")"))
        ))

;; Optional: bind C-c c to org-capture
(global-set-key (kbd "C-c c") #'org-capture)

(provide 'capture)
;;; capture.el ends here





;; ===============( to add )===========================
        ;; 📨 Inbox Entry
;;("i" "Inbox" entry
         ;;(file+headline "~/org/inbox.org" "Inbox")
        ;; "* TODO %?\n:CREATED: %U\n")

      
        ;; ;; 🔖 Stakeholder Task with Weight Prompt
        ;; ("T" "Stakeholder Task" entry
        ;;  (file+headline "~/org/projects.org" "Stakeholder Tasks")
        ;;  "* TODO %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:STAKEHOLDER: %^{Weight|3|2|1}\n:END:\n%?\n")

        ;; ;; 🧠 Zettelkasten Note
        ;; ("z" "Zettel" entry
        ;;  (file+datetree "~/org/qxs.org")
        ;;  "* %^{Title}\n:PROPERTIES:\n:ID: %(org-id-uuid)\n:CREATED: %U\n:END:\n%?\n")

        ;; ;; 📅 Scheduled Work Block
        ;; ("s" "Scheduled Block" entry
        ;;  (file+headline "~/org/daily.org" "Schedule")
        ;;  "* %^{Title}\nSCHEDULED: %^t\n:CREATED: %U\n%?")

        ;; ;; 🛠️  Workbench Log Entry
        ;; ("w" "Workbench Log" entry
        ;;  (file+datetree "~/org/workbench.org")
        ;;  "* %U %^{Log Title}\n%?\n")

        ;; ;; 🧩 Backlog Item
        ;; ("b" "Backlog Item" entry
        ;;  (file+headline "~/org/projects.org" "Backlog")
        ;;  "* TODO %^{Title}\n:CREATED: %U\n:BACKLOG: t\n%?\n")

        ;; ;; 💡 Raw Idea
        ;; ("x" "Idea" entry
        ;;  (file+headline "~/org/inbox.org" "Ideas")
        ;;  "* %^{Idea Title}\n:CREATED: %U\n:IDEA: t\n%?\n")
        ;; ))
