from src.database.models import Template

class TemplateRepository:
    """Repository for Template-related database operations."""

    @staticmethod
    async def get_template_by_id(template_id: int):
        """Fetch a template by its ID."""
        return await Template.get(idTemplate=template_id)

    @staticmethod
    async def get_all_templates():
        """Fetch all templates."""
        return await Template.all()

    @staticmethod
    async def create_template(template_data: dict):
        """Create a new template."""
        template = await Template.create(**template_data)
        return template

    @staticmethod
    async def update_template(template_id: int, updated_data: dict):
        """Update an existing template."""
        await Template.filter(idTemplate=template_id).update(**updated_data)

    @staticmethod
    async def delete_template(template_id: int):
        """Delete a template by ID."""
        await Template.filter(idTemplate=template_id).delete()
