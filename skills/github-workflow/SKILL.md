---
name: github-workflow
description: GitHub repo inceleme, branch, commit, pull request, review ve güvenli değişiklik yönetiminde kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [github, git, pull-request, review]
---
# GitHub Workflow
Repo kurallarını (HERMES.md/AGENTS.md/CONTRIBUTING) önce oku.
Ana dala doğrudan push yapma. Her görev için ayrı kısa branch aç.
Değişiklik öncesi güncel dosyayı oku; binary ve secret commit etme.
Commit mesajı görevi açıklasın. Testleri çalıştır.
PR açıklamasında amaç, değişen dosyalar, test sonucu ve kalan riskleri yaz.
Kullanıcı açıkça istemedikçe PR merge etme, force-push veya history rewrite yapma.
