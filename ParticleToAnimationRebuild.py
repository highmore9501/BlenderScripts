import bpy


class ParticleToAnimationOperator(bpy.types.Operator):
    bl_idname = 'opr.object_particle_to_animation_operator'
    bl_label = 'Object ParticleToAnimation'

    # Set these to False if you don't want to key that property.
    KEYFRAME_LOCATION = True
    KEYFRAME_ROTATION = True
    KEYFRAME_SCALE = True
    KEYFRAME_VISIBILITY = True  # Viewport and render visibility.

    def create_objects_for_particles(self, context, obj, ps):
        # Duplicate the given object for every particle and return the duplicates.
        # Use instances instead of full copies.
        obj_list = []

        mesh = obj.data
        for i, _ in enumerate(ps.particles):
            dupli = bpy.data.objects.new(
                name="particle.{:03d}".format(i),
                object_data=mesh)
            context.scene.objects.link(dupli)
            obj_list.append(dupli)

        return obj_list

    def match_and_keyframe_objects(self, context, ps, obj_list):
        # Match and keyframe the objects to the particles for every frame in the
        # given range.
        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end

        for frame in range(start_frame, end_frame + 1):
            context.scene.frame_set(frame)
            for p, obj in zip(ps.particles, obj_list):
                self.match_object_to_particle(p, obj)
                self.keyframe_obj(obj)

    def match_object_to_particle(self, p, obj):
        # Match the location, rotation, scale and visibility of the object to
        # the particle.
        loc = p.location
        rot = p.rotation
        size = p.size
        if p.alive_state == 'ALIVE':
            vis = True
        else:
            vis = False
        obj.location = loc
        # Set rotation mode to quaternion to match particle rotation.
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = rot
        obj.scale = (size, size, size)
        obj.hide = not (vis)
        obj.hide_render = not (vis)

    def keyframe_obj(self, obj):
        # Keyframe location, rotation, scale and visibility if specified.
        if self.KEYFRAME_LOCATION:
            obj.keyframe_insert("location")
        if self.KEYFRAME_ROTATION:
            obj.keyframe_insert("rotation_quaternion")
        if self.KEYFRAME_SCALE:
            obj.keyframe_insert("scale")
        if self.KEYFRAME_VISIBILITY:
            obj.keyframe_insert("hide")
            obj.keyframe_insert("hide_render")

    def execute(self, context):
        # Assume only 2 objects are selected.
        # The active object should be the one with the particle system.

        obj = context.scene.objects[context.scene.Obj]
        ps_obj = context.scene.objects[context.scene.ps_obj]
        ps = ps_obj.particle_systems[0]  # Assume only 1 particle system is present.

        obj_list = self.create_objects_for_particles(context, obj, ps)
        self.match_and_keyframe_objects(context, ps, obj_list)

        return {'FINISHED'}
