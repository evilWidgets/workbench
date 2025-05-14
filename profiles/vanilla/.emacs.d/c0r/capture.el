;;; capture.el --- WorkBench capture templates -*- lexical-binding: t; -*-

(provide 'capture)

(setq org-capture-templates
      `(
        ;; 📨 Inbox Entry
        ("i" "Inbox" entry
         (file+headline "~/org/inbox.org" "Inbox")
         "* TODO %?\n:CREATED: %U\n")

        ;; ✅ Generic Task
        ("t" "Task" entry
         (file+headline "~/org/projects.org" "Tasks")
         "* TODO %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:END:\n%?\n")

        ;; 🔖 Stakeholder Task with Weight Prompt
        ("T" "Stakeholder Task" entry
         (file+headline "~/org/projects.org" "Stakeholder Tasks")
         "* TODO %^{Title}\n:PROPERTIES:\n:CREATED: %U\n:STAKEHOLDER: %^{Weight|3|2|1}\n:END:\n%?\n")

        ;; 🧠 Zettelkasten Note
        ("z" "Zettel" entry
         (file+datetree "~/org/qxs.org")
         "* %^{Title}\n:PROPERTIES:\n:ID: %(org-id-uuid)\n:CREATED: %U\n:END:\n%?\n")

        ;; 📅 Scheduled Work Block
        ("s" "Scheduled Block" entry
         (file+headline "~/org/daily.org" "Schedule")
         "* %^{Title}\nSCHEDULED: %^t\n:CREATED: %U\n%?")

        ;; 🛠️ Workbench Log Entry
        ("w" "Workbench Log" entry
         (file+datetree "~/org/workbench.org")
         "* %U %^{Log Title}\n%?\n")

        ;; 🧩 Backlog Item
        ("b" "Backlog Item" entry
         (file+headline "~/org/projects.org" "Backlog")
         "* TODO %^{Title}\n:CREATED: %U\n:BACKLOG: t\n%?\n")

        ;; 💡 Raw Idea
        ("x" "Idea" entry
         (file+headline "~/org/inbox.org" "Ideas")
         "* %^{Idea Title}\n:CREATED: %U\n:IDEA: t\n%?\n")
        ))
