# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AuditLog(models.Model):
    _name = 'audit.log'
    _description = 'Audit Log for Performance Management'
    _order = 'create_date desc'
    _rec_name = 'action_description'

    # Basic Information
    action_description = fields.Char(
        string='Action Description',
        required=True,
        help="Brief description of the action performed"
    )
    
    details = fields.Html(
        string='Details',
        help="Detailed information about the change"
    )
    
    # User and Timestamp
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user,
        help="User who performed the action"
    )
    
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        default=fields.Datetime.now,
        help="When the action was performed"
    )
    
    # Record Information
    model_name = fields.Char(
        string='Model',
        required=True,
        help="Model name of the affected record"
    )
    
    record_id = fields.Integer(
        string='Record ID',
        required=True,
        help="ID of the affected record"
    )
    
    record_name = fields.Char(
        string='Record Name',
        help="Name/title of the affected record"
    )
    
    # Action Type
    action_type = fields.Selection([
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('submit', 'Submit'),
        ('cancel', 'Cancel'),
        ('archive', 'Archive'),
        ('restore', 'Restore'),
        ('bulk_update', 'Bulk Update'),
        ('import', 'Import'),
        ('export', 'Export'),
        ('other', 'Other'),
    ], string='Action Type', required=True, default='update')
    
    # Change Information
    field_name = fields.Char(
        string='Field Name',
        help="Name of the field that was changed (if applicable)"
    )
    
    old_value = fields.Text(
        string='Old Value',
        help="Previous value before the change"
    )
    
    new_value = fields.Text(
        string='New Value',
        help="New value after the change"
    )
    
    # Context Information
    ip_address = fields.Char(
        string='IP Address',
        help="IP address of the user"
    )
    
    user_agent = fields.Text(
        string='User Agent',
        help="Browser/client information"
    )
    
    session_id = fields.Char(
        string='Session ID',
        help="User session identifier"
    )
    
    # Related Records (for performance management context)
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        help="Related programme (if applicable)"
    )
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Directorate',
        help="Related directorate (if applicable)"
    )
    
    # Computed fields
    model_display_name = fields.Char(
        string='Model Display Name',
        compute='_compute_model_display_name',
        store=True
    )
    
    @api.depends('model_name')
    def _compute_model_display_name(self):
        for record in self:
            if record.model_name:
                try:
                    model = self.env[record.model_name]
                    record.model_display_name = model._description or record.model_name
                except KeyError:
                    record.model_display_name = record.model_name
            else:
                record.model_display_name = ''
    
    @api.model
    def log_action(self, model_name, record_id, action_type, action_description, 
                   details=None, field_name=None, old_value=None, new_value=None,
                   record_name=None, programme_id=None, directorate_id=None):
        """
        Create an audit log entry
        
        Args:
            model_name (str): Name of the model
            record_id (int): ID of the record
            action_type (str): Type of action performed
            action_description (str): Description of the action
            details (str, optional): Detailed information
            field_name (str, optional): Name of changed field
            old_value (str, optional): Previous value
            new_value (str, optional): New value
            record_name (str, optional): Name of the record
            programme_id (int, optional): Related programme ID
            directorate_id (int, optional): Related directorate ID
        """
        # Get request context for additional information
        request = getattr(self.env, 'request', None)
        ip_address = None
        user_agent = None
        session_id = None
        
        if request:
            ip_address = request.httprequest.environ.get('REMOTE_ADDR')
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT')
            session_id = request.session.sid if hasattr(request, 'session') else None
        
        # Create the audit log entry
        return self.create({
            'model_name': model_name,
            'record_id': record_id,
            'action_type': action_type,
            'action_description': action_description,
            'details': details,
            'field_name': field_name,
            'old_value': str(old_value) if old_value is not None else None,
            'new_value': str(new_value) if new_value is not None else None,
            'record_name': record_name,
            'programme_id': programme_id,
            'directorate_id': directorate_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'session_id': session_id,
        })
    
    @api.model
    def log_field_change(self, record, field_name, old_value, new_value, action_description=None):
        """
        Log a field change for a record
        
        Args:
            record: The record that was changed
            field_name (str): Name of the changed field
            old_value: Previous value
            new_value: New value
            action_description (str, optional): Custom description
        """
        if not action_description:
            field_label = record._fields.get(field_name).string if field_name in record._fields else field_name
            action_description = f"{field_label} updated"
        
        # Get programme and directorate context if available
        programme_id = None
        directorate_id = None
        
        if hasattr(record, 'programme_id') and record.programme_id:
            programme_id = record.programme_id.id
        elif hasattr(record, 'parent_programme_id') and record.parent_programme_id:
            programme_id = record.parent_programme_id.id
            
        if hasattr(record, 'directorate_id') and record.directorate_id:
            directorate_id = record.directorate_id.id
        
        return self.log_action(
            model_name=record._name,
            record_id=record.id,
            action_type='update',
            action_description=action_description,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            record_name=record.display_name,
            programme_id=programme_id,
            directorate_id=directorate_id
        )
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.action_description} - {record.user_id.name} ({record.timestamp.strftime('%Y-%m-%d %H:%M')})"
            result.append((record.id, name))
        return result
