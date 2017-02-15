import json

from social.tests.backends.oauth import OAuth2Test


class NationBuilderOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.nationbuilder.NationBuilderOAuth2'
    user_data_url = 'https://foobar.nationbuilder.com/api/v1/people/me'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer',
        'created_at': 1422937981,
        'expires_in': 2592000
    })
    user_data_body = json.dumps({
        'person': {
            'twitter_followers_count': None,
            'last_name': 'Bar',
            'rule_violations_count': 0,
            'linkedin_id': None,
            'recruiter_id': None,
            'membership_expires_at': None,
            'donations_raised_count': 0,
            'last_contacted_at': None,
            'prefix': None,
            'profile_content_html': None,
            'email4': None,
            'email2': None,
            'availability': None,
            'occupation': None,
            'user_submitted_address': None,
            'could_vote_status': None,
            'state_upper_district': None,
            'salesforce_id': None,
            'van_id': None,
            'phone_time': None,
            'profile_content': None,
            'auto_import_id': None,
            'parent_id': None,
            'email4_is_bad': False,
            'twitter_updated_at': None,
            'email3_is_bad': False,
            'bio': None,
            'party_member': None,
            'unsubscribed_at': None,
            'fax_number': None,
            'last_contacted_by': None,
            'active_customer_expires_at': None,
            'federal_donotcall': False,
            'warnings_count': 0,
            'first_supporter_at': '2015-02-02T19:30:28-08:00',
            'previous_party': None,
            'donations_raised_amount_this_cycle_in_cents': 0,
            'call_status_name': None,
            'marital_status': None,
            'facebook_updated_at': None,
            'donations_count': 0,
            'note_updated_at': None,
            'closed_invoices_count': None,
            'profile_headline': None,
            'fire_district': None,
            'mobile_normalized': None,
            'import_id': None,
            'last_call_id': None,
            'donations_raised_amount_in_cents': 0,
            'facebook_address': None,
            'is_profile_private': False,
            'last_rule_violation_at': None,
            'sex': None,
            'full_name': 'Foo Bar',
            'last_donated_at': None,
            'donations_pledged_amount_in_cents': 0,
            'primary_email_id': 1,
            'media_market_name': None,
            'capital_amount_in_cents': 500,
            'datatrust_id': None,
            'precinct_code': None,
            'email3': None,
            'religion': None,
            'first_prospect_at': None,
            'judicial_district': None,
            'donations_count_this_cycle': 0,
            'work_address': None,
            'is_twitter_follower': False,
            'email1': 'foobar@gmail.com',
            'email': 'foobar@gmail.com',
            'contact_status_name': None,
            'mobile_opt_in': True,
            'twitter_description': None,
            'parent': None,
            'tags': [],
            'first_volunteer_at': None,
            'inferred_support_level': None,
            'banned_at': None,
            'first_invoice_at': None,
            'donations_raised_count_this_cycle': 0,
            'is_donor': False,
            'twitter_location': None,
            'email1_is_bad': False,
            'legal_name': None,
            'language': None,
            'registered_at': None,
            'call_status_id': None,
            'last_invoice_at': None,
            'school_sub_district': None,
            'village_district': None,
            'twitter_name': None,
            'membership_started_at': None,
            'subnations': [],
            'meetup_address': None,
            'author_id': None,
            'registered_address': None,
            'external_id': None,
            'twitter_login': None,
            'inferred_party': None,
            'spent_capital_amount_in_cents': 0,
            'suffix': None,
            'mailing_address': None,
            'is_leaderboardable': True,
            'twitter_website': None,
            'nbec_guid': None,
            'city_district': None,
            'church': None,
            'is_profile_searchable': True,
            'employer': None,
            'is_fundraiser': False,
            'email_opt_in': True,
            'recruits_count': 0,
            'email2_is_bad': False,
            'county_district': None,
            'recruiter': None,
            'twitter_friends_count': None,
            'facebook_username': None,
            'active_customer_started_at': None,
            'pf_strat_id': None,
            'locale': None,
            'twitter_address': None,
            'is_supporter': True,
            'do_not_call': False,
            'profile_image_url_ssl': 'https://d3n8a8pro7vhmx.cloudfront.net'
                                     '/assets/icons/buddy.png',
            'invoices_amount_in_cents': None,
            'username': None,
            'donations_amount_in_cents': 0,
            'is_volunteer': False,
            'civicrm_id': None,
            'supranational_district': None,
            'precinct_name': None,
            'invoice_payments_amount_in_cents': None,
            'work_phone_number': None,
            'phone': '213.394.4623',
            'received_capital_amount_in_cents': 500,
            'primary_address': None,
            'is_possible_duplicate': False,
            'invoice_payments_referred_amount_in_cents': None,
            'donations_amount_this_cycle_in_cents': 0,
            'priority_level': None,
            'first_fundraised_at': None,
            'phone_normalized': '2133944623',
            'rnc_regid': None,
            'twitter_id': None,
            'birthdate': None,
            'mobile': None,
            'federal_district': None,
            'donations_to_raise_amount_in_cents': 0,
            'support_probability_score': None,
            'invoices_count': None,
            'nbec_precinct_code': None,
            'website': None,
            'closed_invoices_amount_in_cents': None,
            'home_address': None,
            'school_district': None,
            'support_level': None,
            'demo': None,
            'children_count': 0,
            'updated_at': '2015-02-02T19:30:28-08:00',
            'membership_level_name': None,
            'billing_address': None,
            'is_ignore_donation_limits': False,
            'signup_type': 0,
            'precinct_id': None,
            'rnc_id': None,
            'id': 2,
            'ethnicity': None,
            'is_survey_question_private': False,
            'middle_name': None,
            'author': None,
            'last_fundraised_at': None,
            'state_file_id': None,
            'note': None,
            'submitted_address': None,
            'support_level_changed_at': None,
            'party': None,
            'contact_status_id': None,
            'outstanding_invoices_amount_in_cents': None,
            'page_slug': None,
            'outstanding_invoices_count': None,
            'first_recruited_at': None,
            'county_file_id': None,
            'first_name': 'Foo',
            'facebook_profile_url': None,
            'city_sub_district': None,
            'has_facebook': False,
            'is_deceased': False,
            'labour_region': None,
            'state_lower_district': None,
            'dw_id': None,
            'created_at': '2015-02-02T19:30:28-08:00',
            'is_prospect': False,
            'priority_level_changed_at': None,
            'is_mobile_bad': False,
            'overdue_invoices_count': None,
            'ngp_id': None,
            'do_not_contact': False,
            'first_donated_at': None,
            'turnout_probability_score': None
        },
        'precinct': None
    })

    def test_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_NATIONBUILDER_SLUG': 'foobar'
            })
        self.do_login()

    def test_partial_pipeline(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_NATIONBUILDER_SLUG': 'foobar'
            })
        self.do_partial_pipeline()
