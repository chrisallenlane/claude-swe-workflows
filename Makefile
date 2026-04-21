REPO := chrisallenlane/claude-swe-workflows

.PHONY: release
release:
ifndef VERSION
	$(error VERSION is required. Usage: make release VERSION=v1.2.0)
endif
	git tag $(VERSION)
	git push origin refs/tags/$(VERSION)
	@PREV=$$(git describe --tags --abbrev=0 $(VERSION)^ 2>/dev/null) && \
		NOTES=$$(git log --pretty=format:'- %s' "$$PREV"..$(VERSION)) || \
		NOTES=$$(git log --pretty=format:'- %s' $(VERSION)); \
	: "# Gitea auto-creates a bare release row when the tag is pushed; delete it so tea release create can insert the real one with notes" ; \
	tea release delete --login gitea --repo $(REPO) --confirm $(VERSION) >/dev/null 2>&1 || true; \
	tea release create \
		--login gitea \
		--repo $(REPO) \
		--tag $(VERSION) \
		--title $(VERSION) \
		--note "$$NOTES" && \
	gh release create $(VERSION) \
		--repo $(REPO) \
		--title $(VERSION) \
		--notes "$$NOTES"
