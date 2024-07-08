from app.models import Member, Mitra, ActivityList

def get_achievements(request):
    try:
        # count total member
        total_member = Member.objects.count()
        # count total mitra
        total_mitra = Mitra.objects.count()
        # count total activity
        total_activity = ActivityList.objects.count()
        context = {
            'total_member': total_member,
            'total_mitra': total_mitra,
            'total_activity': total_activity,
        }
        return context
    except Exception as e:
        return 'Gagal mengambil data pencapaian: ' + str(e)