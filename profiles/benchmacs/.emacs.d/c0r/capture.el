;;; capture.el --- WorkBench capture templates -*- lexical-binding: t; -*-

(provide 'capture)

(setq org-capture-templates
      ;;====================================
      ;; 🗃️ Inbox Items 
      '(("i" "Inbox" entry
         (file+headline "~/workbench/org/inbox.org" "Inbox")
         "* TODO %?\n %U\n"
	 :after-finalize (lambda()
			   (call-process
			    "/home/ben/workbench/workbench_env/bin/python"
			    nil 
			    nil 
			    nil
			    "/home/ben/workbench/tools/post_sort_inbox.py"
			    "--urgent" "--projects")
			   )))
)
      ;;         ;; 📥 Backlog Item
;;         ("b" "Backlog" entry
;;          (file+headline "~/org/backlog.org" "Backlog")
;;          "* TODO %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:BACKLOG: t\n:END:\n%?\n")

;;         ;; 💡 Idea Entry
;;         ("x" "Idea" entry
;;          (file+headline "~/org/idea.org" "Ideas")
;;          "* %^{Idea Title}\n:PROPERTIES:\n:CREATED: %U\n:IDEA: t\n:END:\n%?\n")

;;         ;; 📂 Project Task
;;         ("p" "Project Task" entry
;;          (file+headline "~/org/projects.org" "Tasks")
;;          "* TODO %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:END:\n%?\n")

;;         ;; ⏭️  Next Action
;;         ("n" "Next Action" entry
;;          (file+headline "~/org/next_actions.org" "Next Actions")
;;          "* NEXT %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:END:\n%?\n")
;;         )
;; )


